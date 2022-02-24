from .helpers.file import get_policy, get_role
from plugin.utils.file import interpolate_json_template
from aws_cdk import core as cdk
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam


class Lambda(cdk.Stack):
    """
    TO DO
    Args:
        cdk ([type]): [description]
    """

    def create_lambda_for_schema_validation(self, name: str, registry: str,  region: str):

        role = iam.CfnRole(
            self,
            f'{name}-api-lambda-role',
            role_name=f'{name}-api-lambda-role',
            assume_role_policy_document=get_role("OsDataRoleLambda"),
            policies=[iam.CfnRole.PolicyProperty(
                policy_document=interpolate_json_template(
                    get_policy("OsDataPolicyLambdaRegistry"),
                    {
                        "AwsAccount": self.account,
                        "AwsRegion": region,
                        "RegistryName": registry
                    }
                ),
                policy_name=f'{name}-api-lambda-policy'
            )]
        )

        lambda_function_name = f'{name}-api-lambda-schema'
        bucket = s3.Bucket.from_bucket_arn(
            self,
            f'import-{name}-bucket-assets',
            f'arn:aws:s3:::{self.account}-{name}-gateway-assets'
        )

        lambda_fn = lambda_.CfnFunction(
            self,
            lambda_function_name,
            code=lambda_.CfnFunction.CodeProperty(
                s3_bucket=bucket.bucket_name,
                s3_key=f'{name}-api-lambda.zip'
            ),
            description="Lambda function used for data schema validation",
            function_name=lambda_function_name,
            handler="main.main",
            runtime="python3.9",
            reserved_concurrent_executions=25,
            memory_size=1024,
            timeout=10,
            role=role.attr_arn,
            tags=[cdk.CfnTag(
                key="name",
                value=lambda_function_name
            )],
            tracing_config=lambda_.CfnFunction.TracingConfigProperty(
                mode="Active"
            )

        )
        lambda_fn.add_depends_on(role)
        return lambda_fn

    def create_bucket_for_lambda_assets(self, name: str):
        return s3.Bucket(
            self,
            id=f'dp-{name}',
            bucket_name=name,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=False
        )
