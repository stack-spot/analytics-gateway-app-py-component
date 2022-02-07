import click
from plugin.usecase.apigateway.main import DataApiGatewayUseCase
from plugin.infrastructure.resource.aws.cdk.main import AwsCdk
from plugin.domain.manifest import Manifest


@click.group()
def apply():
    pass # We just need a click.group to create our command


@apply.command('data-api-gateway')
@click.option('-f', '--file', 'path')
def create_data_gateway(path: str):
    manifest = Manifest(manifest=path)
    DataApiGatewayUseCase(AwsCdk()).create(manifest.api_gateway)
