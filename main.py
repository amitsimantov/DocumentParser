import os

from utils.config import Config, ConfigObj
from utils.db.db_layer import DBLayer
from utils.db.collection_layer import CollectionFactory
from utils.tools import get_args
from utils.logger import Logger

from app.parser import DocumentParser
from app.validator import DocumentValidator, ValidationStatus
from app.settings import DOCUMENTS, DISCREPANCIES


class DocumentParserApp:

    def __init__(self, config: ConfigObj, db: DBLayer, dir_path: str):
        self._db = db
        self._config = config
        self._dir_path = dir_path
        self._logger = Logger('main-app-logger').get_logger()

    def run(self):
        try:
            # CollectionFactory.empty_all(self._db)

            files_list = [os.path.join(self._dir_path, entry) for entry in os.listdir(self._dir_path) if
                          os.path.isfile(os.path.join(self._dir_path, entry))]

            documents_data = []
            discrepancies_data = []
            for file in files_list:
                try:
                    parser = DocumentParser()
                    parsed_data = parser.parse(file)
                    documents_data.append(parsed_data.dict())

                    validator = DocumentValidator(min_title_length=self._config.min_title_length,
                                                  max_creation_date=self._config.max_creation_date,
                                                  max_row_sum=self._config.max_row_sum)
                    validation_result = validator.validate(parsed_data)
                    discrepancies_data.extend(validation_result.discrepancies)

                except Exception as e:
                    self._logger.error(f'Failed processing file: {file}, {e}')

            CollectionFactory.insert_many_to_collection(collection_name=DOCUMENTS, data=documents_data, db=self._db)
            CollectionFactory.insert_many_to_collection(collection_name=DISCREPANCIES, data=discrepancies_data, db=self._db)

        except Exception as e:
            self._logger.error(f'An unexpected error occurred: {e}')


if __name__ == '__main__':
    args = get_args()
    app_config = Config.get_config(args)
    app_db = DBLayer(db_uri=app_config.db_uri,
                     db_name=app_config.db_name).get_db()

    app = DocumentParserApp(config=app_config,
                            db=app_db,
                            dir_path=args.PATH)
    app.run()
