from utils.logger import Logger
from app.settings import DOCUMENTS, DISCREPANCIES


class BaseCollectionHandler:

    def __init__(self, db):
        self._db = db
        self._logger = Logger(f'base-collection-logger').get_logger()
        self._collection = None

    def insert(self, data):
        if not data:
            self._logger.warning('Received an empty data set. Ignoring.')
            return

        try:
            result = self._collection.insert_one(data)
            self._logger.info(result)

        except Exception as e:
            self._logger.error(f'Failed inserting data to db! {e}')

    def insert_many(self, data):
        if not data:
            self._logger.warning('Received an empty data set. Ignoring.')
            return

        try:
            result = self._collection.insert_many(data)
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


class DocumentCollectionHandler(BaseCollectionHandler):

    def __init__(self, db):
        super(DocumentCollectionHandler, self).__init__(db)
        self._collection = self._db[DOCUMENTS]
        self._logger = Logger(f'{DOCUMENTS}-collection-logger').get_logger()


class DiscrepancyCollectionHandler(BaseCollectionHandler):

    def __init__(self, db):
        super(DiscrepancyCollectionHandler, self).__init__(db)
        self._collection = self._db[DISCREPANCIES]
        self._logger = Logger(f'{DISCREPANCIES}-collection-logger').get_logger()


class CollectionFactory:

    HANDLERS_MAP = {DISCREPANCIES: DiscrepancyCollectionHandler,
                    DOCUMENTS: DocumentCollectionHandler}

    _logger = Logger(f'collection-factory-logger').get_logger()

    @classmethod
    def _validate_collection_name(cls, collection_name):
        if collection_name not in cls.HANDLERS_MAP:
            cls._logger.error('Incorrect collection name!')
            raise ValueError(f"Unknown collection name: {collection_name}")

    @classmethod
    def _get_collection_handler(cls, collection_name, db):
        cls._validate_collection_name(collection_name)
        return cls.HANDLERS_MAP[collection_name](db)

    @classmethod
    def insert_many_to_collection(cls, collection_name, data, db):
        if not data:
            cls._logger.warning('Received an empty data set. Ignoring.')
            return

        try:
            collection_handler = cls._get_collection_handler(collection_name, db)
            collection_handler.insert_many(data)
            cls._logger.info(f'Finished inserting data to collection: {collection_name}')
        except Exception as e:
            cls._logger.error(f'Failed inserting data to collection: {collection_name}, {e}')

    @classmethod
    def empty_all(cls, db):
        for c in cls.HANDLERS_MAP:
            try:
                cls.HANDLERS_MAP[c](db).empty()
                cls._logger.info(f'Emptied db successfully!')

            except Exception as e:
                cls._logger.error(f'Failed emptying collection: {c}, {e}')
