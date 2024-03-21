import os
from pydantic import BaseModel
from datetime import date

from utils.logger import Logger


class ConfigObj(BaseModel):
    db_name: str
    db_uri: str
    min_title_length: int
    max_creation_date: date
    max_row_sum: int


class Config:

    _logger = Logger('config-logger').get_logger()

    @classmethod
    def get_config(cls, args):
        try:
            config = ConfigObj(
                db_name=os.getenv('DB_NAME'),
                db_uri=os.getenv('DB_URI'),
                min_title_length=args.N,
                max_creation_date=args.D,
                max_row_sum=args.SUM
            )
            return config

        except ValueError as e:
            cls._logger.error(f'Failed parsing config - invalid environment variable! {e}')
            exit(1)

        except Exception as e:
            cls._logger.error(f'Failed parsing config - check for missing environment variables! {e}')
            exit(1)
