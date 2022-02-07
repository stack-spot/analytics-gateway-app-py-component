from .interface import KinesisInterface
from function.utils import logger
from function.domain.exceptions import PutRecordError
from botocore.client import ClientError
import boto3

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


    def put_record(self, name: str, record: str, partition_key: str):
        try:
            response = self.kinesis.put_record(
                StreamName=name,
                Data=record,
                PartitionKey=partition_key)
            logger.info("Put record in stream %s.", name)
            return response
        except ClientError:
            logger.exception("Couldn't put record in stream %s.", name)
            raise  PutRecordError("Couldn't put record in stream %s.", name)
