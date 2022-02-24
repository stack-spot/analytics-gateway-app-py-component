from aws_cdk import (core, assertions)
from plugin.infrastructure.resource.aws.cdk.stacks.lambda_stack import Lambda


def test_aws_cdk_create_lambda_assets():
    app = core.App()
    stack_name = "create-lambda-assets-stack"
    lambda_stack = Lambda(app, stack_name)
    bucket_name = "bucket-name"

    lambda_stack.create_bucket_for_lambda_assets(bucket_name)

    template = assertions.Template.from_stack(lambda_stack)
    template.has_resource_properties("AWS::S3::Bucket", {
        "BucketName": bucket_name,
        "BucketEncryption": {
            "ServerSideEncryptionConfiguration": [
                {
                    "ServerSideEncryptionByDefault": {
                        "SSEAlgorithm": "AES256"
                    }
                }
            ]
        },
    })


def test_aws_cdk_create_lambda_for_schema_validation():
    app = core.App()
    stack_name = "create-lambda-schema-validation-stack"
    lambda_stack = Lambda(app, stack_name)
    bucket_name = "bucket-name"
    registry = "registry-1"
    region = "us-east-1"

    lambda_stack.create_lambda_for_schema_validation(
        bucket_name, registry, region)

    template = assertions.Template.from_stack(lambda_stack)
    template.has_resource_properties("AWS::Lambda::Function", {
        "Code": {
            "S3Bucket": {
                "Fn::Join": [
                    "",
                    [
                        {
                            "Ref": "AWS::AccountId"
                        },
                        "-bucket-name-gateway-assets"
                    ]
                ]
            },
            "S3Key": "bucket-name-api-lambda.zip"
        },
        "Role": {
            "Fn::GetAtt": [
                "bucketnameapilambdarole",
                "Arn"
            ]
        },
        "Description": "Lambda function used for data schema validation",
        "FunctionName": "bucket-name-api-lambda-schema",
        "Handler": "main.main",
        "MemorySize": 1024,
        "ReservedConcurrentExecutions": 25,
        "Runtime": "python3.9",
        "Tags": [
            {
                "Key": "name",
                "Value": "bucket-name-api-lambda-schema"
            }
        ],
        "Timeout": 10,
        "TracingConfig": {
            "Mode": "Active"
        }
    })

    template.has_resource_properties("AWS::IAM::Role", {
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        },
        "Policies": [
            {
                "PolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "AWSGlueSchemaRegistryReadonlyAccess",
                            "Effect": "Allow",
                            "Action": [
                                "glue:GetRegistry",
                                "glue:ListRegistries",
                                "glue:GetSchema",
                                "glue:ListSchemas",
                                "glue:GetSchemaByDefinition",
                                "glue:GetSchemaVersion",
                                "glue:ListSchemaVersions",
                                "glue:GetSchemaVersionsDiff",
                                "glue:CheckSchemaVersionValidity",
                                "glue:QuerySchemaVersionMetadata",
                                "glue:GetTags"
                            ],
                            "Resource": [
                                "*"
                            ]
                        },
                        {
                            "Sid": "AWSLogsSchemaRegistryReadonlyAccess",
                            "Effect": "Allow",
                            "Action": [
                                "logs:DescribeLogGroups",
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents"
                            ],
                            "Resource": [
                                "*"
                            ]
                        },
                        {
                            "Sid": "AWSPutSchemaRegistryReadonlyAccess",
                            "Action": "kinesis:PutRecords",
                            "Resource": {
                                "Fn::Join": [
                                    "",
                                    [
                                      "arn:aws:kinesis:us-east-1:",
                                      {
                                          "Ref": "AWS::AccountId"
                                      },
                                        f":stream/{registry}-*"
                                    ]
                                ]
                            },
                            "Effect": "Allow"
                        }
                    ]
                },
                "PolicyName": f"{bucket_name}-api-lambda-policy"
            }
        ],
        "RoleName": f"{bucket_name}-api-lambda-role"
    })
