from datetime import datetime, date
from typing import Sequence, Mapping, Any

def str_to_object_date(date_str: str) -> date:
    """
    Convert a date string in 'YYYY-MM-DD' format to a `date` object.

    Args:
        date_str (str): Date string in the format 'YYYY-MM-DD'.

    Returns:
        date: Corresponding `date` object.
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def object_date_to_str(date_obj: datetime) -> str:
    """
    Convert a `datetime` object to a string in 'DD-MM-YYYY' format.

    Args:
        date_obj (datetime): The datetime object to convert.

    Returns:
        str: The formatted date string.
    """
    return date_obj.strftime("%d-%m-%Y")

def converted_rowmapping_to_dict(result: Sequence[Mapping[Any, Any]]) -> list[dict[str, Any]]:
    """
    Convert a sequence of row mappings (e.g., from SQLAlchemy) to a list of dictionaries,
    converting any 'delivery_date' field from datetime to string.

    Args:
        result (Sequence[Mapping[Any, Any]]): Sequence of row mappings with column-value pairs.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing each row,
        with 'delivery_date' formatted as a string if present.
    """
    orders = []

    for row in result:
        d = dict(row)

        if "delivery_date" in d and isinstance(d["delivery_date"], datetime):
            d["delivery_date"] =  object_date_to_str(d["delivery_date"])
        orders.append(d)

    return orders
