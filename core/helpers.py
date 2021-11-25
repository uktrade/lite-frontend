from urllib.parse import urlencode
from functools import lru_cache


def dummy_quote(string, safe="", encoding=None, errors=None):
    return string


def convert_dict_to_query_params(dictionary):
    return urlencode(dictionary, doseq=True, quote_via=dummy_quote)


def convert_parameters_to_query_params(dictionary):
    if "request" in dictionary:
        del dictionary["request"]
    return "?" + convert_dict_to_query_params({key: value for key, value in dictionary.items() if value is not None})


def convert_value_to_query_param(key: str, value):
    if value is None:
        return ""
    return urlencode({key: value}, doseq=True, quote_via=dummy_quote)


def parse_boolean(value):
    if isinstance(value, str):
        if value.lower() in ("yes", "true"):
            return True
        else:
            return False
    return value


cache = lru_cache  # TODO: Remove this once we hit python3.8


class cached_property:
    """
    SRC: https://stackoverflow.com/questions/4037481/caching-class-attributes-in-python

    TODO: Remove this once we hit python3.8
    """

    def __init__(self, factory):
        self._attr_name = factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        attr = self._factory(instance)
        setattr(instance, self._attr_name, attr)
        return attr
