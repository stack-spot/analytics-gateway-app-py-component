from abc import ABCMeta, abstractmethod


class Route53Interface(metaclass=ABCMeta):
    """
    TO DO
    """

    @abstractmethod
    def get_hosted_zone(self, zone_id: str):
        raise NotImplementedError

    @abstractmethod
    def not_exists_record(self, zone_id: str, name: str):
        raise NotImplementedError
