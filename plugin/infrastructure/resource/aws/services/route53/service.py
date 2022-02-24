from .interface import Route53Interface
from botocore.client import ClientError
from plugin.utils.logging import logger
import boto3


class Route53Service(Route53Interface):
    """
    TO DO

    Args:
        Route3Interface ([type]): [description]
    """

    def __init__(self):
        self.route53 = boto3.client('route53')

    def get_hosted_zone(self, zone_id: str):
        try:
            res = self.route53.get_hosted_zone(Id=zone_id)
            return res["HostedZone"] if "HostedZone" in res else None
        except ClientError as err:
            logger.error('exp: %s', err)
            return None

    def not_exists_record(self, zone_id: str, name: str):
        try:
            res = self.route53.list_resource_record_sets(HostedZoneId=zone_id)
            records = res["ResourceRecordSets"]
            for record in records:
                record_name = record["Name"].split(".")[0]
                if record_name == name:
                    return False
            return True
        except ClientError as err:
            logger.error('exp: %s', err)
            return False
