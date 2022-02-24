from botocore.stub import Stubber
from plugin.infrastructure.resource.aws.services.route53.service import Route53Service
import boto3


route53 = boto3.client('route53')
stubber = Stubber(route53)

class TestRoute53Service(Route53Service):
    __test__ = False

    def __init__(self):
        self.route53 = route53


def test_route53_init():
    service = Route53Service()
    service.route53
    assert str(type(service.route53)) == str(type(boto3.client('route53')))


def test_get_hosted_zone():
    response = {
            'HostedZone': {
                'Id': 'zone-id',
                'Name': 'zone-name',
                'CallerReference': 'string',
                'Config': {
                    'Comment': 'string',
                    'PrivateZone': True
                    },
                'ResourceRecordSetCount': 123,
                'LinkedService': {
                    'ServicePrincipal': 'string',
                    'Description': 'string'
                    }
                }
            }
    stubber.add_response(
            "get_hosted_zone",
            response,
            { "Id": "zone-id" })
    stubber.activate()
    route53_service = TestRoute53Service()
    res = route53_service.get_hosted_zone("zone-id")
    if res is not None:
        assert res["Id"] == response["HostedZone"]["Id"]


def test_get_hosted_zone_empty():
    stubber.add_client_error("get_hosted_zone")
    stubber.activate()
    route53_service = TestRoute53Service()
    res = route53_service.get_hosted_zone("zone-id")
    assert res is None


def test_not_exists_record():
    domain = 'test.domain.com'
    response = {
            'ResourceRecordSets': [
                {
                    'Name': domain,
                    'Type': 'SOA',
                    'SetIdentifier': 'string',
                    'Weight': 123,
                    'Region': 'us-east-1',
                    'GeoLocation': {
                        'ContinentCode': 'string',
                        'CountryCode': 'string',
                        'SubdivisionCode': 'string'
                        },
                    'Failover': 'PRIMARY',
                    'MultiValueAnswer': True,
                    'TTL': 123,
                    'ResourceRecords': [
                        {
                            'Value': 'string'
                            },
                        ],
                    'AliasTarget': {
                        'HostedZoneId': 'string',
                        'DNSName': 'string',
                        'EvaluateTargetHealth': True
                        },
                    'HealthCheckId': 'string',
                    'TrafficPolicyInstanceId': 'string'
                    },
                ],
            'IsTruncated': True,
            'MaxItems': 'string'
            }
    stubber.add_response("list_resource_record_sets", response, { "HostedZoneId": "zone-id" })
    stubber.activate()
    route53_service = TestRoute53Service()
    res = route53_service.not_exists_record("zone-id", "test-1")
    assert res is True


def test_not_exists_record_exists():
    domain = 'test.domain.com'
    response = {
            'ResourceRecordSets': [
                {
                    'Name': domain,
                    'Type': 'SOA',
                    'SetIdentifier': 'string',
                    'Weight': 123,
                    'Region': 'us-east-1',
                    'GeoLocation': {
                        'ContinentCode': 'string',
                        'CountryCode': 'string',
                        'SubdivisionCode': 'string'
                        },
                    'Failover': 'PRIMARY',
                    'MultiValueAnswer': True,
                    'TTL': 123,
                    'ResourceRecords': [
                        {
                            'Value': 'string'
                            },
                        ],
                    'AliasTarget': {
                        'HostedZoneId': 'string',
                        'DNSName': 'string',
                        'EvaluateTargetHealth': True
                        },
                    'HealthCheckId': 'string',
                    'TrafficPolicyInstanceId': 'string'
                    },
                ],
            'IsTruncated': True,
            'MaxItems': 'string'
            }
    stubber.add_response("list_resource_record_sets", response, { "HostedZoneId": "zone-id" })
    stubber.activate()
    route53_service = TestRoute53Service()
    res = route53_service.not_exists_record("zone-id", "test")
    assert res is False


def test_no_exists_record_exception():
    stubber.add_client_error("list_resource_record_sets") 
    stubber.activate()
    route53_service = TestRoute53Service()
    res = route53_service.not_exists_record("zone-id", "test")
    assert res is False
