import os
from datetime import date, datetime


def convert_str_to_date_obj(date_string: str) -> date | None:
    try:
        return datetime.strptime(date_string, os.getenv('DATE_FORMAT')).date()

    except ValueError:
        raise

    except Exception:
        raise
