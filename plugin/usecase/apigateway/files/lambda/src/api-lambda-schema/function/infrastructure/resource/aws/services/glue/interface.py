from abc import ABCMeta, abstractmethod

class GlueInterface(metaclass=ABCMeta):
    """
    TO DO
    """

    @abstractmethod
    def get_schema(self, **knargs):
        raise NotImplementedError
    
    @abstractmethod
    def get_schema_by_definition(self, **knargs):
        raise NotImplementedError
    
    @abstractmethod
    def get_schema_version(self, **knargs):
        raise NotImplementedError