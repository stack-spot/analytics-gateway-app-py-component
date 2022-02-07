from abc import ABCMeta, abstractmethod


class PutStreamInterface(metaclass=ABCMeta):
		@abstractmethod
		def put_stream_transaction(self, stream_name: str, record: dict,) -> dict:
			raise NotImplementedError