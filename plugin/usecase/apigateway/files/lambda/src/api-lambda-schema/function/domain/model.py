from dataclasses import dataclass


@dataclass(frozen=True)
class EventsModel:
    __slots__ = [
        'data_product',
        'schema_name',
        'schema_version'
    ]

    data_product: str
    schema_name: str
    schema_version: str
