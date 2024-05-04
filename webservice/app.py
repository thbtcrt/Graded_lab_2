import boto3
import os
from dotenv import load_dotenv
from typing import Union
import logging
from fastapi import FastAPI, Request, status, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


from getSignedUrl import getSignedUrl

load_dotenv()

app = FastAPI()
logger = logging.getLogger("uvicorn")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logger.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Post(BaseModel):
    title: str
    body: str


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))

# Endpoint to create a new post
@app.post("/posts")
async def post_a_post(post: Post, authorization: str | None = Header(default=None)):

    logger.info(f"title : {post.title}")
    logger.info(f"body : {post.body}")
    logger.info(f"user : {authorization}")

    # Extract user from authorization header
    user = authorization.split(":")[0] if authorization else None

    # Save post to DynamoDB
    item = {
        "user": user,
        "title": post.title,
        "body": post.body
    }
    table.put_item(Item=item)

    return {"message": "Post created successfully"}

# Endpoint to get all posts
@app.get("/posts")
async def get_all_posts(user: Union[str, None] = None):

    # If user provided, query posts by user
    if user:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user').eq(user)
        )
        posts = response['Items']
    # Otherwise, get all posts
    else:
        response = table.scan()
        posts = response['Items']

    return posts

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
