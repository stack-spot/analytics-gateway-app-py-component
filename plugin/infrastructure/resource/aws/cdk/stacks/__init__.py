from aws_cdk import core as cdk

from .api_gateway import ApiGateway
from .lambda_stack import Lambda 

class Stack(ApiGateway, Lambda):
    """
    TO DO
    Args:
        ApiGateway ([type]): [description]
    """

    def __init__(self, scope: cdk.Construct,
                 construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
