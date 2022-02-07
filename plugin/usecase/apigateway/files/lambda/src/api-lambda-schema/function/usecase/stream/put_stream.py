from function.infrastructure.resource.aws.services.main import SDK
from .interface import PutStreamInterface

class PutStream(PutStreamInterface):

    def __init__(self, region: str):
        self.cloud_adapter = SDK()
        self.region = region
        

    def put_stream_transaction(self, stream_name: str, record: dict,) -> dict:
        self.cloud_adapter.put_record(stream_name, record, "default", self.region)

