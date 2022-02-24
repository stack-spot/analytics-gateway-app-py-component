from abc import ABCMeta, abstractmethod


class KinesisInterface(metaclass=ABCMeta):
    """
    TO DO
    """

    @abstractmethod
    def put_records(self, name: str, records: list, partition_key: str) -> None:
        raise NotImplementedError
