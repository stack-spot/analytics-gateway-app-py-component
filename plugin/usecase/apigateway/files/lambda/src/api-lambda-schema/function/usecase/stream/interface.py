from abc import ABCMeta, abstractmethod


class PutStreamInterface(metaclass=ABCMeta):
    @abstractmethod
    def put_stream_transaction(self, stream_name: str, records: list) -> None:
        raise NotImplementedError
