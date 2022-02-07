from .interface import ACMInterface
from botocore.client import ClientError
import boto3


class ACMService(ACMInterface):
    """
    TO DO

    Args:
        ACMInterface ([type]): [description]
    """

    def __init__(self):
        self.acm = boto3.client('acm')

    def list_certificates(self):
        try:
            return self.acm.list_certificates()
        except ClientError as err:
            print('exp: ', err)
            return None
