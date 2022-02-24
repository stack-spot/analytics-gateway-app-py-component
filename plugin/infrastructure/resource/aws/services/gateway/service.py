from .interface import ApiGatewayInterface
from botocore.client import ClientError
from plugin.utils.logging import logger
import boto3


class ApiGatewayService(ApiGatewayInterface):
    """
    TO DO

    Args:
        ApiGatewayInterface ([type]): [description]
    """

    def __init__(self, region: str):
        self.api_gateway = boto3.client('apigateway', region_name=region)

    def create_custom_domain(self, domain_name: str, cert_arn: str, type_: str):
        try:
            response = self.api_gateway.create_domain_name(
                domainName=domain_name,
                certificateArn=cert_arn,
                securityPolicy='TLS_1_2',
                endpointConfiguration={'types': [type_]}
            )
            print(f"{response['domainName']} created")
        except ClientError as err:
            logger.error(
                "Unexpected error while creating custom domain: %s", err)

    def not_exists_api_gateway(self, name: str):
        try:
            res = self.api_gateway.get_rest_apis()
            items = res["items"]
            response = True
            for item in items:
                if item["name"] == name:
                    response = False
                    break
            return response
        except ClientError as err:
            logger.error(
                "Unexpected error while check api gateway exists: %s", err)
            return None
