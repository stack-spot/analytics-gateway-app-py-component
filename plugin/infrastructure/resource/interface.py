from abc import ABCMeta, abstractmethod
from plugin.domain.manifest import ApiGateway


class DataApiGatewayCloudInterface(metaclass=ABCMeta):
    """
    TO DO
    """
    @abstractmethod
    def create_setup(self, api_gateway: ApiGateway):
        """
        TO DO
        """
        raise NotImplementedError

    @abstractmethod
    def create_assets(self, api_gateway: ApiGateway):
        """
        TO DO
        """
        raise NotImplementedError

    @abstractmethod
    def create_function(self, name: str, registry: str, region: str):
        """
        TO DO
        """
        raise NotImplementedError
