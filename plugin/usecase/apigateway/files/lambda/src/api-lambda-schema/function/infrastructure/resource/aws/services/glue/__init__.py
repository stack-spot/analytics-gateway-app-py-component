from .service import Glue as glue_service
import json


class Glue:
    """
    TO DO
    """
    @staticmethod
    def get_schema_version(registry: str, schema: str, schema_version: int, region: str) -> dict:
        glue = glue_service(region)
        return glue.get_schema_version(SchemaId={'RegistryName': registry, 'SchemaName': schema},
                                            SchemaVersionNumber={'VersionNumber': schema_version})

    @staticmethod
    def get_schema(registry: str, schema: str, region: str) -> dict:
        glue = glue_service(region)
        return glue.get_schema(SchemaId={'RegistryName':registry,'SchemaName':schema})