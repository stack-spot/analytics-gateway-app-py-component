from .interface import KinesisInterface
from function.utils import logger
from function.domain.exceptions import PutRecordsError
from botocore.client import ClientError
import boto3
import json

logger = logger(__name__)


class Kinesis(KinesisInterface):
    """
    TO DO

    Args:
        KinesisInterface ([type]): [description]
    """

    def __init__(self, region: str):
        session = boto3.Session()
        self.kinesis = session.client(
            "kinesis", region_name=region)

    def put_records(self, name: str, records: list, partition_key: str) -> None:
        try:
            records_to_put = [
                {
                    'Data': json.dumps(record).encode('utf-8'),
                    'PartitionKey': partition_key
                } for record in records
            ]

            self.kinesis.put_records(
                StreamName=name,
                Records=records_to_put
            )

            logger.info("Put %d records in stream %s.", len(records_to_put), name)
        except ClientError:
            logger.exception("Couldn't put records in stream %s.", name)
            raise PutRecordsError("Couldn't put records in stream %s.", name)
