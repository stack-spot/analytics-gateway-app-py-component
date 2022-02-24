from .service import Kinesis as kns_service


class Kinesis:
    """
    TO DO
    """
    @staticmethod
    def put_records(name: str, records: list, partition_key: str,  region: str) -> None:
        kns = kns_service(region)
        kns.put_records(name, records, partition_key)
