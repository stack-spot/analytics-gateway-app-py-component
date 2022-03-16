from plugin.infrastructure.resource.interface import DataApiGatewayCloudInterface
from plugin.usecase.apigateway.interface import DataApiGatewayInterface
from plugin.infrastructure.resource.aws.services.main import SDK
from plugin.domain.manifest import ApiGateway
from plugin.utils.string import kebab


class DataApiGatewayUseCase(DataApiGatewayInterface):
    """
    TODO
    """
    cloud: DataApiGatewayCloudInterface

    def __init__(self, cloud: DataApiGatewayCloudInterface) -> None:
        self.cloud = cloud

    def create(self, api_gateway: ApiGateway):
        cloud_service = SDK()
        k_apigateway_name = kebab(api_gateway.name)
        if api_gateway.record is not None and cloud_service.not_exists_record(api_gateway.record.zone_id, f"analytics-{k_apigateway_name}"):
            self.cloud.create_setup(api_gateway)
        return True
