import boto3
import sys
from botocore.exceptions import UnauthorizedSSOTokenError
from botocore.client import BaseClient, ClientError
from function.utils import logger
from .kinesis import Kinesis
from .glue import Glue


logger(__name__)


class SDK(Glue, Kinesis):
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
