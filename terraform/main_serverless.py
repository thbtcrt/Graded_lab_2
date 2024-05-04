#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput, TerraformAsset, AssetType
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.default_vpc import DefaultVpc
from cdktf_cdktf_provider_aws.default_subnet import DefaultSubnet
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket
from cdktf_cdktf_provider_aws.s3_bucket_cors_configuration import S3BucketCorsConfiguration, S3BucketCorsConfigurationCorsRule
from cdktf_cdktf_provider_aws.dynamodb_table import DynamodbTable, DynamodbTableAttribute
from cdktf_cdktf_provider_aws.data_aws_caller_identity import DataAwsCallerIdentity

class ServerlessStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        AwsProvider(self, "AWS", region="us-east-1")

        account_id = DataAwsCallerIdentity(self, "account_id").account_id

        bucket = S3Bucket(
            self, "bucket",
            bucket_prefix="mycdktfbucket",
            force_destroy=True,
            versioning={"enabled": True}
        )

        S3BucketCorsConfiguration(
            self, "cors",
            bucket=bucket.id,
            cors_rule=[S3BucketCorsConfigurationCorsRule(
                allowed_headers=["*"],
                allowed_methods=["GET", "HEAD", "PUT"],
                allowed_origins=["*"]
            )]
        )

        dynamo_table = DynamodbTable(
            self, "DynamodDB-table",
            name="MyDynamoDB",
            hash_key="user",
            range_key="id",
            attribute=[
                DynamodbTableAttribute(name="id", type="S"),
                DynamodbTableAttribute(name="user", type="S")
            ],
            billing_mode="PROVISIONED",
            read_capacity=5,
            write_capacity=5
        )

        TerraformOutput(self, "s3_bucket_name",
                        value=bucket.bucket_domain_name,
                        description="Name of the S3 bucket")

        TerraformOutput(self, "dynamodb_table_name",
                        value=dynamo_table.name,
                        description="Name of the DynamoDB table")


app = App()
ServerlessStack(app, "cdktf_serverless")
app.synth()

# cdktf deploy -a "pipenv run python3 main_serverless.py"