import logging
import sys
from pythonjsonlogger import jsonlogger
from .config import Config

def setup_logging():
    """
    Sets up JSON logging format for the service.
    """
    logger = logging.getLogger()
    
    logger.setLevel(Config.LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger