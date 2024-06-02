import logging
from os import getenv

logger = logging.getLogger('graphw00f')

def setup_logger():
    logger.addHandler(logging.StreamHandler())

    level = logging.INFO
    if getenv('DEBUG'):
        level = logging.DEBUG
    elif getenv('LOG_LEVEL'):
        level = getenv('LOG_LEVEL')

    logger.setLevel(level)
