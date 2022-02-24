from botocore.stub import Stubber
from plugin.infrastructure.resource.aws.services.acm import ACMService
import boto3


acm = boto3.client('acm', region_name='us-east-1')
stubber = Stubber(acm)

class TestACMService(ACMService):
    __test__ = False

    def __init__(self):
        self.acm = acm


def test_acm_init():
    service = ACMService("us-east-1")
    assert str(type(service.acm)) == str(type(acm))


def test_list_certificates_empty():
    stubber.add_client_error("list_certificates")
    stubber.activate()
    service = TestACMService()
    assert service.list_certificates() is None

def test_get_certificate_by_hosted_zone():
    response ={
            'NextToken': 'string',
            'CertificateSummaryList': [
                {
                    'CertificateArn': 'arn:aws:acm:us-east-1:123456789012:certificate/cb32ea34-6302-4f43-8r53-7053cdd49097',
                    'DomainName': '*.domain-name.com'
                    },
                ]
            }
    stubber.add_response("list_certificates", response)
    stubber.activate()
    service = TestACMService()
    res = service.get_certificate_by_hosted_zone({ "Name": "domain-name.com" })
    assert res["DomainName"] is not None


def test_get_certificate_by_hosted_zone_empty():
    response ={
            'NextToken': 'string',
            'CertificateSummaryList': [
                {
                    'CertificateArn': 'arn:aws:acm:us-east-1:123456789012:certificate/cb32ea34-6302-4f43-8r53-7053cdd49097',
                    'DomainName': '*.domain-name.com'
                    },
                ]
            }
    stubber.add_response("list_certificates", response)
    stubber.activate()
    service = TestACMService()
    res = service.get_certificate_by_hosted_zone({ "Name": "domain.com" })
    assert res == {}
