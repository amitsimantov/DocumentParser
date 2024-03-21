import re
from bs4 import BeautifulSoup
from pydantic import BaseModel

from utils.logger import Logger


class ParsedData(BaseModel):
    document_id:            str | None
    file_name:              str | None
    title:                  str | None
    header:                 list | None
    body:                   list | None
    footer:                 str | None
    country_of_creation:    str | None
    date_of_creation:       str | None


class DocumentParser:

    def __init__(self):
        self._logger = Logger('parser-logger').get_logger()

    @staticmethod
    def clean(cell):
        return cell.get_text(strip=True)

    @staticmethod
    def read_file(file):
        with open(file) as f:
            content = f.read()
        return content

    def parse(self, file: str):
        """
        Parses html document.
        :param file path
        :return: ParsedData object
        """
        self._logger.info(f'Reading file: {file}')
        html_content = self.read_file(file)

        self._logger.info(f'Parsing file: {file}')
        soup = BeautifulSoup(html_content, 'lxml')
        table = soup.find('table')
        if not table:
            raise Exception(f'File: {file} does not contain table!')
        file_name = file.split('/')[-1]
        document_id = table.get('id', None)
        title = self.clean(table.caption) if table.caption else None
        header = [self.clean(th) for th in table.find_all('th')][1:] if table.find_all('th') else None
        body = [[self.clean(td) for td in row.find_all('td')] for row in table.find_all('tr')[1:]]
        footer = self.clean(table.tfoot.tr.td) if table.tfoot and table.tfoot.tr and table.tfoot.tr.td else None
        creation_info = re.search(r'Creation:\s*(\d{1,2}[a-zA-Z]{3}\d{4})\s*(.+)', footer) if footer else None
        date, country = creation_info.groups() if creation_info else (None, None)

        parsed_data = ParsedData(
            document_id=document_id,
            file_name=file_name,
            title=title,
            header=header,
            body=body,
            footer=footer,
            country_of_creation=country,
            date_of_creation=date
        )

        self._logger.info(f'Finished parsing file: {file}')
        return parsed_data





