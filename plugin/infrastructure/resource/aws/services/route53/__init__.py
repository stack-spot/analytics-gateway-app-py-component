from .service import Route53Service


class Route53:
    """
    TO DO
    """
    @staticmethod
    def get_hosted_zone(zone_id: str) -> dict:
        hosted_zone = Route53Service().get_hosted_zone(zone_id)
        return hosted_zone if hosted_zone is not None else {}

    @staticmethod
    def not_exists_record(zone_id: str, name: str):
        return Route53Service().not_exists_record(zone_id, name)

