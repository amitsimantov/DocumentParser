from enum import Enum
from pydantic import BaseModel
from datetime import date
from typing import Optional

from utils.logger import Logger
from utils.tools import convert_str_to_date_obj
from parser import ParsedData


class ValidationStatus(Enum):
    VALID = 'VALID'
    INVALID = 'INVALID'
    ERROR = 'ERROR'
    NOT_FOUND = 'NOT_FOUND'
    NOT_PROCESSED = 'NOT_PROCESSED'


class DiscrepancyLocation(Enum):
    TITLE = 'TITLE'
    BODY = 'BODY'
    CREATION_DATE = 'CREATION_DATE'


class DiscrepancyType(Enum):
    MISSING = 'MISSING'
    INVALID_VALUE = 'INVALID_VALUE'


class Discrepancy(BaseModel):
    type:           DiscrepancyType
    location:       DiscrepancyLocation
    description:    Optional[str] = None

    class Config:
        use_enum_values = True


class ValidationResult(BaseModel):
    status:         ValidationStatus
    discrepancies:  list[Discrepancy]

    class Config:
        use_enum_values = True


class DocumentValidator:

    def __init__(self, min_length: int, max_date: date, max_sum: int):
        self._min_length = min_length
        self._max_date = max_date
        self._max_sum = max_sum
        self._logger = Logger('validator-logger').get_logger()

        self._status = ValidationStatus.VALID
        self._discrepancies = list()

    def validate(self, parsed_data: ParsedData):
        self._logger.info(f'Validating document: {parsed_data.document_id}')
        self._validate_title(parsed_data.title)
        self._validate_creation_date(parsed_data.date_of_creation)
        self._validate_body(parsed_data.body)

        if self._discrepancies:
            self._status = ValidationStatus.INVALID

        self._logger.info(f'Finished validating document: {parsed_data.document_id}')

        return ValidationResult(status=self._status,
                                discrepancies=self._discrepancies)

    def _validate_body(self, body: list | None):
        if not body:
            self._discrepancies.append(Discrepancy(type=DiscrepancyType.MISSING,
                                                   location=DiscrepancyLocation.BODY))

        elif sum([int(x) for x in body[0][1:]]) > self._max_sum:
            self._discrepancies.append(Discrepancy(type=DiscrepancyType.INVALID_VALUE,
                                                   location=DiscrepancyLocation.BODY,
                                                   description=f'sum of first row is greater than: {self._max_sum}'))

    def _validate_creation_date(self, date_of_creation: str | None):
        if not date_of_creation:
            self._discrepancies.append(Discrepancy(type=DiscrepancyType.MISSING,
                                                   location=DiscrepancyLocation.CREATION_DATE))
            return

        try:
            date_of_creation = convert_str_to_date_obj(date_of_creation)
            if not date_of_creation or date_of_creation > self._max_date:
                self._discrepancies.append(Discrepancy(type=DiscrepancyType.INVALID_VALUE,
                                                       location=DiscrepancyLocation.CREATION_DATE,
                                                       description=f'creation date is later than: {self._max_sum}'))

        except ValueError:
            self._discrepancies.append(Discrepancy(type=DiscrepancyType.INVALID_VALUE,
                                                   location=DiscrepancyLocation.CREATION_DATE,
                                                   description=f'creation date is not in the correct format'))

    def _validate_title(self, title: str | None):
        if not title:
            self._discrepancies.append(Discrepancy(type=DiscrepancyType.MISSING,
                                                   location=DiscrepancyLocation.TITLE))

        elif len(title) < self._min_length:
            self._discrepancies.append(Discrepancy(type=DiscrepancyType.INVALID_VALUE,
                                                   location=DiscrepancyLocation.TITLE,
                                                   description=f'title length is shorter than: {self._min_length}'))

