from .service import ACMService


class ACM:
    """
    TO DO
    """
    @staticmethod
    def get_certificate_by_hosted_zone(hosted_zone) -> dict:
        res = ACMService().list_certificates()
        if res is not None:
            certs = res["CertificateSummaryList"]
            certificates_list = [
                cert for cert in certs
                if cert["DomainName"] == hosted_zone["Name"]
                or cert["DomainName"] == f"*.{hosted_zone['Name']}"
                or f"{cert['DomainName']}." == hosted_zone["Name"]
            ]
            return certificates_list[0] if len(certificates_list) > 0 else {}
        return {}
