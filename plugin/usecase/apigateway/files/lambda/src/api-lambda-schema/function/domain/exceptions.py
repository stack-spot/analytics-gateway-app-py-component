#!/usr/bin/python3


class APIError(Exception):
    """
    Generic Exception.
    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Something Went Wrong!"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return str(self.message)


class PutRecordsError(APIError):
    """
    Exception for when could not put records with boto3 sdk.
    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Couldn't put records."):
        self.message = message
        super().__init__(self.message)
