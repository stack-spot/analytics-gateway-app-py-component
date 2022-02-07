from function.infrastructure.resource.aws.services.main import SDK
from .interface import SchemaValidationInterface
from avro.io import validate
from avro.schema import parse

class SchemaValidation(SchemaValidationInterface):

    def __init__(self, region: str):
        self.cloud_adapter = SDK()
        self.region = region

    def validate_schema_version(self, registry: str, schema: str, record: dict, schema_version) -> int: 
        schema_version = self.__get_schema_latest(registry, schema) if schema_version == 'latest' else schema_version
        reponse = self.cloud_adapter.get_schema_version(registry, schema, int(schema_version), self.region)
        validate(parse(reponse['SchemaDefinition']), record, raise_on_error=True)
        return int(reponse['VersionNumber'])

    def __get_schema_latest(self, registry: str, schema: str) -> dict:
        response = self.cloud_adapter.get_schema(registry, schema, self.region)
        return response['LatestSchemaVersion']

