#!/usr/bin/python3
from function.domain.model import EventModel
from function.domain.message import ResponseMessage
from function.usecase.schema.validation import SchemaValidation
from function.usecase.stream.put_stream import PutStream
from function.environment import Environments
import json

environments = Environments()

def parse_body(record: dict):
        record['body'] = json.loads(record['body'])
        event = {
            'event_id' : record['body']['EventID'],
            'event_time' : record['body']['EventTime'],
            'data_product': record['pathParameters']['dataProduct'],
            'schema_name': record['pathParameters']['schema'],
            'schema_version': record['pathParameters']['schemaVersion'],
            'event_data' : json.loads(record['body']['EventData'])
        }
        return event
    
def main(event, context):
    try:
        message = parse_body(event)
        body = EventModel(**message)
        val_ = SchemaValidation(environments.region)
        message['schema_version'] = val_.validate_schema_version(body.data_product, body.schema_name, body.event_data, body.schema_version)
        put_ = PutStream(environments.region)
        put_.put_stream_transaction(f'{body.data_product}-{body.schema_name}-kinesis',  message)
        
        return ResponseMessage.rep_200(
                    message=f"Put record in stream {body.data_product}-{body.schema_name}-kinesis.", 
                    type='EventTransaction', 
                    category='DataSchema', 
                    id=body.event_id).format_report
    
    except Exception as err: 
        return ResponseMessage.rep_400(
                message=str(err), 
                type='EventTransactionError', 
                category='DataSchema', 
                id='ex00000001').format_report
   
