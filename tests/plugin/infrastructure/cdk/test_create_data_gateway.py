import string
import random
import pytest
from aws_cdk import core
from unittest import TestCase
from plugin.infrastructure.resource.aws.cdk.stacks.api_gateway import ApiGateway
from plugin.domain.manifest import Manifest
import json


class CdkStackApiGateway(TestCase):

    @staticmethod
    def __random_string(letter, size: int):
        return ''.join(random.choice(letter) for _ in range(size))

    @pytest.fixture(autouse=True)
    def plugin_manifest(self):
        self.manifest = Manifest({
            "api_gateway": {
                "name": "my-gateway",
                "region": "us-east-1",
                "type": "PRIVATE",
                "auth": {
                    "iam_auth": True,
                    "api_key": True
                },
                "registry": "registry_xxxxxxx",
                "record": {
                    "zone_id": "ZONEID12341234"
                },
                "vpc_endpoint": {
                    "vpc_id": "vpc_xxxxxxx",
                    "subnets_ids": ["sub_xxxxxxx"],
                    "security_group": {
                        "ip_blocks_sg": ["10.0.0.0/21"],
                        "eg_blocks_sg": ["0.0.0.0/0"]
                    }
                }
            }
        })

    @pytest.fixture(autouse=True)
    def cdk_app(self):
        self.app = core.App()
        self.stack_name = f"create-api-gateway-stack-{self.__random_string(letter=string.ascii_letters,size=10)}"
        self.stack = ApiGateway(self.app, self.stack_name)

    def __create_vpc_endpoint(self):
        _security_group = self.stack.create_security_group(
            domain=self.manifest.api_gateway.name,
            eg_blocks_sg=self.manifest.api_gateway.vpc_endpoint.security_group.eg_blocks_sg,
            ip_blocks_sg=self.manifest.api_gateway.vpc_endpoint.security_group.ip_blocks_sg,
            vpc_id=self.manifest.api_gateway.vpc_endpoint.vpc_id
        )

        _vpc_endpoint = self.stack.create_vpc_endpoint(
            domain=self.manifest.api_gateway.name,
            region=self.manifest.api_gateway.region,
            subnet_ids=self.manifest.api_gateway.vpc_endpoint.subnets_ids,
            security_group_id=_security_group.attr_group_id,
            vpc_id=self.manifest.api_gateway.vpc_endpoint.vpc_id
        )
        return _vpc_endpoint

    def test_if_create_data_api_gateway_works(self):
        name = self.__random_string(
            letter=string.ascii_letters,
            size=18)
        self.manifest.api_gateway.name = f"{name}_test"
        _vpc_endpoint = self.__create_vpc_endpoint()
        self.stack.create_api_gateway(
            domain=self.manifest.api_gateway.name,
            vpc_id=self.manifest.api_gateway.vpc_endpoint.vpc_id,
            vpce=_vpc_endpoint,
            region=self.manifest.api_gateway.region,
            type_=self.manifest.api_gateway.type)

        _a_record = self.stack.create_route53_a_record(
                name=self.manifest.api_gateway.name,
                zone_id=self.manifest.api_gateway.record.zone_id,
                zone_name="hosted.example.com",
                vpc_endpoint=_vpc_endpoint
            )
