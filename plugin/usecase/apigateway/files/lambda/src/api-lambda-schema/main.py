#!/usr/bin/python3
from __future__ import annotations
from function.domain.model import EventsModel
from function.domain.message import ResponseMessage
from function.usecase.schema.validation import SchemaValidation
from function.usecase.stream.put_stream import PutStream
from function.environment import Environments
import json

environments = Environments()


def parse_events(data_events: list | dict, datalake_name: str, schema_name: str, schema_version: int) -> list:
    if isinstance(data_events, list):
        events = [
            {
                "event_id": event["EventID"],
                "event_time": event["EventTime"],
                "data_product": datalake_name,
                "schema_name": schema_name,
                "schema_version": schema_version,
                "event_data": json.loads(event["EventData"])
            } for event in data_events
        ]
    elif isinstance(data_events, dict):
        events = [
            {
                "event_id": data_events["EventID"],
                "event_time": data_events["EventTime"],
                "data_product": datalake_name,
                "schema_name": schema_name,
                "schema_version": schema_version,
                "event_data": json.loads(data_events["EventData"])
            }
        ]

    return events


def main(event, context):
    try:
        data_events = json.loads(event["body"])

        body = EventsModel(
            data_product=event["pathParameters"]["datalake_name"],
            schema_name=event["pathParameters"]["schema_name"],
            schema_version=event["pathParameters"]["schema_version"]
        )

        validate = str(event["queryStringParameters"].get(
            "validate", "true")).lower()

        val_ = SchemaValidation(environments.region)
        version = val_.get_schema_version(
            registry=body.data_product,
            schema=body.schema_name,
            version=body.schema_version
        )

        if validate == "true":
            val_.validate_schema_version(
                registry=body.data_product,
                schema=body.schema_name,
                data_events=data_events,
                version=version
            )

            records = parse_events(
                data_events=data_events,
                datalake_name=body.data_product,
                schema_name=body.schema_name,
                schema_version=version
            )
        else:
            records = parse_events(
                data_events=data_events,
                datalake_name=body.data_product,
                schema_name=body.schema_name,
                schema_version=version
            )

        put_ = PutStream(environments.region)
        put_.put_stream_transaction(
            f"{body.data_product}-{body.schema_name}-kinesis",  records)

        return ResponseMessage.resp_200(
            message=f"Put {len(records)} records in stream {body.data_product}-{body.schema_name}-kinesis.",
            type="EventTransaction",
            category="DataSchema",
            id=context.aws_request_id).format_report
    except Exception as err:
        if isinstance(err, KeyError):
            return ResponseMessage.resp_400(
                message=f"Required field not found in the request: {err}",
                type="EventTransactionError",
                category="DataSchema",
                id=context.aws_request_id).format_report

        return ResponseMessage.resp_400(
            message=str(err),
            type="EventTransactionError",
            category="DataSchema",
            id=context.aws_request_id).format_report
