from __future__ import annotations
from function.infrastructure.resource.aws.services.main import SDK
from .interface import SchemaValidationInterface
from avro.io import validate
from avro.schema import parse
import json


class SchemaValidation(SchemaValidationInterface):

    def __init__(self, region: str):
        self.cloud_adapter = SDK()
        self.region = region

    def validate_schema_version(self, registry: str, schema: str, data_events: list | dict, version: int) -> None:
        reponse = self.cloud_adapter.get_schema_version(
            registry, schema, int(version), self.region
        )

        if isinstance(data_events, list):
            for event in data_events:
                validate(
                    parse(reponse["SchemaDefinition"]),
                    json.loads(event["EventData"]),
                    raise_on_error=True
                )

        if isinstance(data_events, dict):
            validate(
                parse(reponse["SchemaDefinition"]),
                json.loads(data_events["EventData"]),
                raise_on_error=True
            )

    def get_schema_version(self, registry: str, schema: str, version: int | str) -> int:
        schema_version = self.__get_schema_latest(
            registry=registry,
            schema=schema
        ) if version == "latest" else version

        return int(schema_version)

    def __get_schema_latest(self, registry: str, schema: str) -> int:
        response = self.cloud_adapter.get_schema(registry, schema, self.region)
        return response["LatestSchemaVersion"]
