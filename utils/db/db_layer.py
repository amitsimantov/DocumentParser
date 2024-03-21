"""
DB Layer for MongoDB.
"""

from pymongo.mongo_client import MongoClient
from utils.logger import Logger


class DBLayer:

    def __init__(self, db_uri, db_name):
        self._logger = Logger('db-layer-logger').get_logger()
        self._client = MongoClient(db_uri)
        self._db = self._client[db_name]

    def get_db(self):
        if self.is_alive():
            return self._db

    def is_alive(self):
        try:
            self._client.admin.command('ping')
            self._logger.info("Successfully connected to MongoDB")
            return True

        except Exception as e:
            self._logger.error(f"Failed to connect to MongoDB: {e}")
            return False
