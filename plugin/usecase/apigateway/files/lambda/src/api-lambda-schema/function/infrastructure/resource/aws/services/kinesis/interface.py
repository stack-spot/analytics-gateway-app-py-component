from abc import ABCMeta, abstractmethod

class KinesisInterface(metaclass=ABCMeta):
    """
    TO DO
    """

    @abstractmethod
    def put_record(self, name: str, record: str, partition_key: str):
        raise NotImplementedError
