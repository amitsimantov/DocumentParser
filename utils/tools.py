import argparse
from datetime import date, datetime

from app.settings import DATE_FORMAT, ARG_DATE_FORMAT


def convert_str_to_date_obj(date_string: str, date_format: str = DATE_FORMAT, exception: Exception = None) -> date | None:
    try:
        return datetime.strptime(date_string, date_format).date()

    except ValueError:
        if exception:
            raise exception

        raise ValueError(f"Not a valid date: '{date_string}'. Expected format: {date_format}.")


def valid_date(date_string):
    msg = f"Not a valid date: '{date_string}'. Expected format: {ARG_DATE_FORMAT}."
    return convert_str_to_date_obj(date_string=date_string,
                                   date_format=ARG_DATE_FORMAT,
                                   exception=argparse.ArgumentTypeError(msg))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-N", type=int, help="an integer value", required=True)
    parser.add_argument("-D", type=valid_date, help="a date in YYYY-MM-DD format", required=True)
    parser.add_argument("-SUM", type=int, help="an integer value", required=True)
    parser.add_argument("-PATH", type=str, help="an integer value", required=True)
    return parser.parse_args()

