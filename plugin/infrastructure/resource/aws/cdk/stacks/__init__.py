from aws_cdk import core as cdk

from .api_gateway import ApiGateway

class Stack(ApiGateway):
    """
    TO DO
    Args:
        ApiGateway ([type]): [description]
    """

    def __init__(self, scope: cdk.Construct,
                 construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
