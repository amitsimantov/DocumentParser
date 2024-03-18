import os
from pydantic import BaseModel, ValidationError
from datetime import date

from utils.logger import Logger
from utils.tools import convert_str_to_date_obj


class ConfigObj(BaseModel):
    db_name: str
    uri: str
    documents_collection: str
    discrepancies_collection: str
    N: int
    D: date
    SUM: int


class Config:

    def __init__(self):
        self._logger = Logger('config-logger').get_logger()

    def get_config(self):
        try:
            config = ConfigObj(
                db_name=os.getenv('DB_NAME'),
                uri=os.getenv('DB_URI'),
                documents_collection=os.getenv('DOCUMENTS_COLLECTION'),
                discrepancies_collection=os.getenv('DISCREPANCIES_COLLECTION'),
                N=os.getenv('N'),
                D=convert_str_to_date_obj(os.getenv('D')),
                SUM=os.getenv('SUM')
            )
            return config

        except ValueError as e:
            self._logger.error(f'Failed parsing config - invalid environment variable! {e}')
            exit(1)

        except Exception as e:
            self._logger.error(f'Failed parsing config - check for missing environment variables! {e}')
            exit(1)
