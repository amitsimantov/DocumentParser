import os

from utils.config import Config
from db.db_layer import DBLayer
from db.collection_layer import DocumentCollection, DiscrepancyCollection
from parser import DocumentParser
from validator import DocumentValidator, ValidationStatus


def main(dir_path: str):
    config = Config().get_config()
    files_list = [os.path.join(dir_path, entry) for entry in os.listdir(dir_path) if
                  os.path.isfile(os.path.join(dir_path, entry))]

    parsed_documents = []
    discrepancies = []

    for file in files_list:
        parser = DocumentParser()
        parsed_data = parser.parse(file)
        parsed_documents.append(parsed_data.dict())

        validator = DocumentValidator(min_length=config.N,
                                      max_date=config.D,
                                      max_sum=config.SUM)
        validation_result = validator.validate(parsed_data)
        if validation_result.status != ValidationStatus.VALID.value:
            discrepancies.extend([{'document_id': parsed_data.document_id,
                                   'discrepancy': {
                                       'type': disc.type,
                                       'location': disc.location,
                                       'description': disc.description}}
                                  for disc in validation_result.discrepancies])

    db = DBLayer(uri=config.uri, db_name=config.db_name).get_db()

    documents_collection = DocumentCollection(db=db, config=config)
    discrepancies_collection = DiscrepancyCollection(db=db, config=config)

    # documents_collection.empty()
    # discrepancies_collection.empty()

    # documents_collection.insert_many(parsed_documents)
    discrepancies_collection.insert_many(discrepancies)


if __name__ == '__main__':
    main('documents')
