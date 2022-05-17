from urllib.parse import urlencode


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


def get_document_data(file):
    return {
        "name": getattr(file, "original_name", file.name),
        "s3_key": file.name,
        "size": int(file.size // 1024) if file.size else 0,  # in kilobytes
    }
