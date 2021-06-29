import re
from core.helpers import format_date


def format_date_fields(data):
    # Convert date
    date_fields = ["first_exhibition_date", "required_by_date"]
    for date_field in date_fields:
        data[date_field] = format_date(data, date_field)
    return data


def split_date_into_components(date, delimiter: str):
    """
    Split a date in the YYYY MM DD format with a given delimiter
    into its year, month, day components
    Useful for prepopulated fields
    """
    split_date = re.split("[%s]" % ("".join(delimiter)), date)
    return split_date[0], split_date[1], split_date[2]


def create_formatted_date_from_components(data):
    return f"{data['year']}-{str(data['month']).zfill(2)}-{str(data['day']).zfill(2)}"
