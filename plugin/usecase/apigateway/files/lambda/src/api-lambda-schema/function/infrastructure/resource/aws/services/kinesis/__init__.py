from .service import Kinesis as kns_service
import json


class Kinesis:
    """
    TO DO
    """
    @staticmethod
    def put_record(name: str, record: dict, partition_key: str,  region: str) -> None:
        kns = kns_service(region)
        return kns.put_record(name, json.dumps(record), partition_key)
