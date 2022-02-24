from .stacks import Stack
from .engine.main import CDKEngine
from plugin.utils.logging import logger
from plugin.domain.manifest import ApiGateway
from plugin.infrastructure.resource.aws.services.main import SDK
from plugin.infrastructure.resource.interface import DataApiGatewayCloudInterface


class AwsCdk(CDKEngine, DataApiGatewayCloudInterface):
    """
    TODO
    """

    def create_setup(self, api_gateway: ApiGateway):
        self.new_app()
        cloud_service = SDK()
        name = api_gateway.name
        stack_name = f'create-{name}-gateway-setup'.replace('_', '-')
        stack = Stack(self.app, stack_name)

        if api_gateway.vpc_endpoint is not None and api_gateway.type == "PRIVATE":
            _security_group = stack.create_security_group(
                name=name,
                eg_blocks_sg=api_gateway.vpc_endpoint.security_group.eg_blocks_sg,
                ip_blocks_sg=api_gateway.vpc_endpoint.security_group.ip_blocks_sg,
                vpc_id=api_gateway.vpc_endpoint.vpc_id
            )

            _vpc_endpoint = stack.create_vpc_endpoint(
                name=name,
                region=api_gateway.region,
                subnet_ids=api_gateway.vpc_endpoint.subnets_ids,
                security_group_id=_security_group.attr_group_id,
                vpc_id=api_gateway.vpc_endpoint.vpc_id
            )

            _vpc_endpoint.add_depends_on(_security_group)

            stack.create_api_gateway(
                account_id=cloud_service.account_id,
                name=name,
                vpc_id=api_gateway.vpc_endpoint.vpc_id,
                vpce=_vpc_endpoint,
                region=api_gateway.region,
                type_=api_gateway.type
            )

            if api_gateway.record is not None:
                hosted_zone = cloud_service.get_hosted_zone(
                    api_gateway.record.zone_id)

                _a_record = stack.create_route53_a_record(
                    name=api_gateway.name,
                    zone_id=api_gateway.record.zone_id,
                    zone_name=hosted_zone["Name"],
                    vpc_endpoint=_vpc_endpoint
                )

                _a_record.add_depends_on(_vpc_endpoint)

        self.deploy(stack_name, api_gateway.region)

    def create_assets(self, api_gateway: ApiGateway):
        self.new_app()
        cloud_service = SDK()
        name = f"{cloud_service.account_id}-{api_gateway.name}-gateway"
        stack_name = f'create-{api_gateway.name}-gateway-assets'.replace('_', '-')
        stack = Stack(self.app, stack_name)

        bucket_logs_exist = cloud_service.check_bucket(f'{name}-logs')
        bucket_assets_exist = cloud_service.check_bucket(f'{name}-assets')

        if not bucket_logs_exist:
            stack.create_bucket_for_lambda_assets(f'{name}-logs')
        else:
            logger.info("Bucket %s-logs already exists.", name)

        if not bucket_assets_exist:
            stack.create_bucket_for_lambda_assets(f'{name}-assets')
        else:
            logger.info("Bucket %s-assets already exists.", name)

        if not bucket_logs_exist or not bucket_assets_exist:
            self.deploy(stack_name, api_gateway.region)

    def create_function(self, name: str, registry: str, region: str):
        self.new_app()
        stack_name = f'create-{name}-api-functions'.replace('_', '-')
        stack = Stack(self.app, stack_name)
        stack.create_lambda_for_schema_validation(name, registry,  region)
        self.deploy(stack_name, region)
