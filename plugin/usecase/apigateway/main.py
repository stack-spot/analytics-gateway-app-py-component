from plugin.infrastructure.resource.interface import DataApiGatewayCloudInterface
from plugin.usecase.apigateway.interface import DataApiGatewayInterface
from plugin.infrastructure.resource.aws.services.main import SDK
from plugin.utils.file import create_lambda_package, get_current_pwd, remove_from_os
from plugin.domain.manifest import ApiGateway


class DataApiGatewayUseCase(DataApiGatewayInterface):
    """
    TODO
    """
    cloud: DataApiGatewayCloudInterface

    def __init__(self, cloud: DataApiGatewayCloudInterface) -> None:
        self.cloud = cloud

    def create(self, api_gateway: ApiGateway):
        cloud_service = SDK()
        self.cloud.create_assets(api_gateway)
        if api_gateway.record is None or cloud_service.not_exists_record(api_gateway.record.zone_id, f"analytics-{api_gateway.name}"):
            lambda_zip_file = f'{api_gateway.name}-api-lambda.zip'
            create_lambda_package(
                "plugin/usecase/apigateway/files/lambda/src/api-lambda-schema", lambda_zip_file)
            cloud_service.upload_object(f'{get_current_pwd()}/{lambda_zip_file}',
                                        f'{cloud_service.account_id}-{api_gateway.name}-gateway-assets', lambda_zip_file)
            remove_from_os(f'{get_current_pwd()}/{lambda_zip_file}')
            self.cloud.create_setup(api_gateway)
        if cloud_service.not_exists_lambda(f"{api_gateway.name}-api-lambda-schema", api_gateway.region):
            self.cloud.create_function(api_gateway.name, api_gateway.registry, api_gateway.region)
        return True
