from __future__ import annotations
from dataclasses import dataclass
from plugin.utils.file import read_yaml
from .validation import ValidationManifest as val_


@dataclass
class Auth:
    """
    TO DO
    """

    iam_auth: bool
    api_key: bool

    def __post_init__(self):
        val_.checking_vars_type(self, iam_auth='bool', api_key='bool')


@dataclass
class Record:
    """
    TO DO
    """

    zone_id: str

    def __post_init__(self):
        val_.checking_vars_type(self, zone_id='str')


@dataclass
class SecurityGroup:
    """
    TO DO
    """

    ip_blocks_sg: list
    eg_blocks_sg: list

    def __post_init__(self):
        val_.checking_vars_type(self, eg_blocks_sg='list', ip_blocks_sg='list')


@dataclass
class VpcEndpoint:
    """
    TO DO
    """

    vpc_id: str
    subnets_ids: list
    security_group: SecurityGroup | dict

    def __post_init__(self):
        val_.checking_vars_type(self, vpc_id='str', subnets_ids='list')
        self.security_group = SecurityGroup(**self.security_group)


@dataclass
class ApiGateway:
    """
    TO DO
    """

    name: str
    region: str
    type: str
    auth: Auth | dict
    registry: str
    vpc_endpoint: VpcEndpoint | dict
    record: Record | None

    def __post_init__(self):
        val_.checking_the_type(self)
        val_.checking_vars_type(
            self, name='str', region='str', type='str', registry='str')
        self.vpc_endpoint = VpcEndpoint(
            **self.vpc_endpoint) if self.vpc_endpoint else self.vpc_endpoint
        self.auth = Auth(**self.auth) if self.auth else self.auth
        self.record = Record(**self.record) if self.record else None


@dataclass
class Manifest:
    """
    TO DO
    """

    api_gateway: ApiGateway

    def __init__(self, manifest) -> None:
        if isinstance(manifest, str):
            file = read_yaml(manifest)
            self.api_gateway = ApiGateway(**file['api_gateway'])
        elif isinstance(manifest, dict):
            self.api_gateway = ApiGateway(**manifest['api_gateway'])
        else:
            raise TypeError
