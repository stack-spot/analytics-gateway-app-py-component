
from .service import LambdaResource


class Lambda:
    """
    TO DO
    """
    @staticmethod
    def not_exists_lambda(name: str, region: str) -> None:
        lakeformation = LambdaResource(region)
        return lakeformation.not_exists_lambda(name)
