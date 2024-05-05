import boto3
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
import os
import uuid
from pydantic import BaseModel
from fastapi import FastAPI, Request, status, Header

load_dotenv()

class Post(BaseModel):
    title: str
    body: str

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv("DYNAMO_TABLE"))
authorization = "palapin"

def post_a_post(authorization: str | None = Header(default=None)):

    # Save post to DynamoDB
    item = {
        "user": f"USER#{authorization}",
        'id': f"POST#{uuid.uuid4()}",
    }

    print(item["user"], item["id"])
    

post_a_post("palapin")