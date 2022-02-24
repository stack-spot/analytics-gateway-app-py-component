from plugin.utils.logging import logger
from .interface import ACMInterface
from botocore.client import ClientError
import boto3


class ACMService(ACMInterface):
    """
    TO DO

    Args:
        ACMInterface ([type]): [description]
    """

    def __init__(self, region: str):
        self.acm = boto3.client('acm', region_name=region)


    def list_certificates(self):
        try:
            return self.acm.list_certificates()
        except ClientError as err:
            logger.error('exp: %s', err)
            return None


    def get_certificate_by_hosted_zone(self, hosted_zone):
        res = self.list_certificates()
        if res is not None:
            certs = res["CertificateSummaryList"]
            certificates_list = [
                cert for cert in certs
                if cert["DomainName"] == hosted_zone["Name"]
                or cert["DomainName"] == f"*.{hosted_zone['Name']}"
                or f"{cert['DomainName']}." == hosted_zone["Name"]
            ]
            return certificates_list[0] if len(certificates_list) > 0 else {}
        return {}
