from .interface import GlueInterface
import boto3


class Glue(GlueInterface):
    """
    TO DO

    Args:
        GlueInterface ([type]): [description]
    """

    def __init__(self, region: str) -> None:
        session = boto3.Session()
        self.glue = session.client(
            "glue", region_name=region)

    def get_schema(self, **knargs):
        return self.glue.get_schema(**knargs)
    
    def get_schema_by_definition(self, **knargs):
        return self.glue.get_schema_by_definition(**knargs)
    
    def get_schema_version(self, **knargs):
        return self.glue.get_schema_version(**knargs)


