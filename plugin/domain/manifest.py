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
        val_.checking_vars_type(self, iam_auth="bool", api_key="bool")


@dataclass
class Record:
    """
    TO DO
    """

    zone_id: str

    def __post_init__(self):
        val_.checking_vars_type(self, zone_id="str")


@dataclass
class SecurityGroup:
    """
    TO DO
    """

    ip_blocks_sg: list
    eg_blocks_sg: list

    def __post_init__(self):
        val_.checking_vars_type(self, eg_blocks_sg="list", ip_blocks_sg="list")


@dataclass
class VpcEndpoint:
    """
    TO DO
    """

    vpc_id: str
    subnets_ids: list
    security_group: SecurityGroup

    def __post_init__(self):
        val_.checking_vars_type(self, vpc_id="str", subnets_ids="list")


@dataclass(frozen=True)
class ApiGateway:
    """
    TO DO
    """

    name: str
    region: str
    type: str
    auth: Auth | None
    registry: str
    vpc_endpoint: VpcEndpoint | None
    record: Record | None

    def __post_init__(self):
        val_.checking_the_type(self)
        val_.checking_vars_type(
            self, name="str", region="str", type="str", registry="str")
        val_.check_special_characters(string=self.name)
        val_.check_special_characters(string=self.registry)


@dataclass
class Manifest:
    """
    TO DO
    """

    api_gateway: ApiGateway

    def __init__(self, manifest) -> None:
        if isinstance(manifest, str):
            manifest_dict = read_yaml(manifest)
        elif isinstance(manifest, dict):
            manifest_dict = manifest
        else:
            raise TypeError

        self.api_gateway = ApiGateway(
            name=manifest_dict["api_gateway"].get("name", None),
            region=manifest_dict["api_gateway"].get("region", "us-east-1"),
            type=str(manifest_dict["api_gateway"].get("type", None)).upper(),
            registry=manifest_dict["api_gateway"].get("registry", None),
            auth=Auth(
                iam_auth=bool(manifest_dict["api_gateway"]["auth"].get("iam_auth", True)),
                api_key=bool(manifest_dict["api_gateway"]["auth"].get("api_key", True))
            ) if "auth" in manifest_dict["api_gateway"] else None,
            record=Record(
                zone_id=manifest_dict["api_gateway"]["record"].get("zone_id", None)
            ) if "record" in manifest_dict["api_gateway"] else None,
            vpc_endpoint=VpcEndpoint(
                vpc_id=manifest_dict["api_gateway"]["vpc_endpoint"].get("vpc_id", None),
                subnets_ids=list(manifest_dict["api_gateway"]["vpc_endpoint"]["subnets_ids"]),
                security_group=SecurityGroup(
                    ip_blocks_sg=list(manifest_dict["api_gateway"]["vpc_endpoint"]["security_group"]["ip_blocks_sg"]),
                    eg_blocks_sg=list(manifest_dict["api_gateway"]["vpc_endpoint"]["security_group"]["eg_blocks_sg"])
                )
            ) if "vpc_endpoint" in manifest_dict["api_gateway"] else None
        )
