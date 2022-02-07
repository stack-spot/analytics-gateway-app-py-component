from abc import ABCMeta, abstractmethod


class ACMInterface(metaclass=ABCMeta):
    """
    TO DO
    """
    
    @abstractmethod
    def list_certificates(self):
        raise NotImplementedError


