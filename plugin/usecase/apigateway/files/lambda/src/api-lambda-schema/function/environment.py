import imp
import os
from .utils import logger

logger(__name__)

class Environments:
    def __init__(self):
        try:
            self.region = os.environ.get("AWS_REGION", "us-east-1")
        except EnvironmentError as e:
            logger.exception(f'Environments Error!\n{e}')
