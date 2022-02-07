from abc import ABCMeta, abstractmethod

class SchemaValidationInterface(metaclass=ABCMeta):
		@abstractmethod
		def validate_schema_version(self, registry: str, schema: str, record: dict, schema_version: int) -> int: 
			raise NotImplementedError