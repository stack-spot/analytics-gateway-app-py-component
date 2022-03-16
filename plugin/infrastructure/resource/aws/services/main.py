import boto3
import sys
from botocore.exceptions import UnauthorizedSSOTokenError
from botocore.client import BaseClient, ClientError
from plugin.utils.logging import logger
from .route53 import Route53
from .acm import ACM
from .gateway import ApiGateway


class SDK(Route53, ACM, ApiGateway):
    """
    TODO
    """
    client: BaseClient

    @property
    def account_id(self):
        try:
            client = boto3.client('sts')
            return client.get_caller_identity().get('Account')
        except UnauthorizedSSOTokenError as sso_error:
            logger.error(sso_error.fmt)
            sys.exit(1)
        except ClientError as err:
            logger.error(err)
            sys.exit(1)
