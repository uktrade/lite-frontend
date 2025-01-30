from urllib.parse import urlencode
from django.http import StreamingHttpResponse
from django.core.exceptions import SuspiciousOperation
from django.utils.http import url_has_allowed_host_and_scheme


class UnsafeURLDestination(SuspiciousOperation):
    pass


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


def is_good_on_application_product_type(good_on_application, product_type):
    try:
        return good_on_application["firearm_details"]["type"]["key"] == product_type
    except (KeyError, TypeError):
        return False


def decompose_date(field_name, date):
    return {
        f"{field_name}_0": date.day,
        f"{field_name}_1": date.month,
        f"{field_name}_2": date.year,
    }


def check_url(request, url):
    url_is_safe = url_has_allowed_host_and_scheme(
        url=url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    )

    if url_is_safe:
        return url
    else:
        raise UnsafeURLDestination(f"URL destination '{url}' was deemed to be unsafe")


def stream_document_response(api_response):
    response = StreamingHttpResponse(api_response.iter_content())
    for header_to_copy in [
        "Content-Type",
        "Content-Disposition",
    ]:
        response.headers[header_to_copy] = api_response.headers[header_to_copy]
    return response


def remove_non_printable_characters(str):
    # Given a string this will remove all non_printable_characters from ascii table
    # Chars 9(/h), 10 (/n), 13(/r) are maintained
    return "".join([c for c in str if ord(c) > 31 or ord(c) in [9, 10, 13]])
