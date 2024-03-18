from utils.logger import Logger


class BaseCollection:

    def __init__(self, db, config):
        self._db = db
        self._config = config
        self._logger = Logger(f'base-collection-logger').get_logger()
        self._collection = None

    def insert(self, data):
        try:
            result = self._collection.insert_one(data)
            self._logger.info(result)

        except Exception as e:
            self._logger.error(f'Failed inserting data to db! {e}')

    def insert_many(self, data_list):
        try:
            result = self._collection.insert_many(data_list)
            self._logger.info(result)

        except Exception as e:
            self._logger.error(f'Failed inserting data to db! {e}')

    def find(self, query):
        try:
            result = self._collection.find(query)
            return result

        except Exception as e:
            self._logger.error(f'Failed searching db! {e}')

    def empty(self):
        try:
            result = self._collection.delete_many({})
            self._logger.info(result)

        except Exception as e:
            self._logger.error(f'Failed emptying collection! {e}')


class DocumentCollection(BaseCollection):

    def __init__(self, db, config):
        super(DocumentCollection, self).__init__(db, config)
        self._collection = self._db[config.documents_collection]
        self._logger = Logger(f'{config.documents_collection}-collection-logger').get_logger()


class DiscrepancyCollection(BaseCollection):

    def __init__(self, db, config):
        super(DiscrepancyCollection, self).__init__(db, config)
        self._collection = self._db[config.discrepancies_collection]
        self._logger = Logger(f'{config.discrepancies_collection}-collection-logger').get_logger()
