import logging

from app.settings import BASE_LOG_FORMAT

class Logger:

    def __init__(self, name: str):
        self._name = name

    def get_logger(self):
        logger = logging.getLogger(self._name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(BASE_LOG_FORMAT)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

