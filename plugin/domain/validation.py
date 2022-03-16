from plugin.utils.logging import logger
from .exceptions import (
    ManifestPrivateVpcEndpointNotFound,
    ManifestRecordNotFound,
    ManifestVpcEndpointNotRequired
)


class ValidationManifest:
    """
    Class for Manifest validation
    """

    @staticmethod
    def checking_vars_type(obj, **fields):
        """
        The function will validate the specified data types that user passed in the input. \n
        input: checking_vars_type(self, name='str', key='value'): \n 
        Key: field name Value: field type
        """
        for key in fields:
            t_key = fields.get(key)
            if type(getattr(obj, key)).__name__ != t_key:
                raise TypeError(
                    f"Data type with specified type is different | Field: {key} Type: {type(getattr(obj, key)).__name__} != Requiret-Type: {t_key}")

    @staticmethod
    def checking_the_type(obj):
        """
        The function will check entries of type PRIVATE/EDGE. \n
        input: checking_the_type(obj):
        """
        if obj.type == 'PRIVATE' and not obj.vpc_endpoint:
            raise ManifestPrivateVpcEndpointNotFound(logger)

        if obj.type in {'EDGE', 'REGIONAL'}:
            if obj.vpc_endpoint:
                raise ManifestVpcEndpointNotRequired(logger)

            if not obj.record:
                raise ManifestRecordNotFound(logger)

    @staticmethod
    def check_special_characters(string: str):
        special_characters = '"!@#$%^&*()-+?=,<>/'

        if any(c in special_characters for c in string):
            raise ValueError(
                'Name must not contains any of these characters: "!@#$%^&*()-+?=,<>/')

