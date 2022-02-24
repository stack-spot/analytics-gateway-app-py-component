from .service import ACMService


class ACM:
    """
    TO DO
    """
    @staticmethod
    def get_certificate_by_hosted_zone(hosted_zone, region):
        return ACMService(region).get_certificate_by_hosted_zone(hosted_zone)
