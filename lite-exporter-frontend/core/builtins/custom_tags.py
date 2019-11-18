import datetime
import json
import re
import warnings

from django import template
from django.template.defaultfilters import stringfilter
from django.templatetags.tz import do_timezone
from django.utils.safestring import mark_safe

from conf.constants import ISO8601_FMT
from conf.settings import env
from core import lite_strings

from lite_content.lite_exporter_frontend import strings

register = template.Library()


@register.simple_tag(name="lcs")
def get_const_string(value):
    """
    Template tag for accessing constants from LITE content library (not for Python use - only HTML)
    """
    warnings.warn("Reference constants from strings directly, only use LCS in HTML files", Warning)
    try:
        return getattr(strings, value)
    except AttributeError:
        return ""


@register.simple_tag
def get_string(value, *args, **kwargs):
    """
    Given a string, such as 'cases.manage.attach_documents' it will return the relevant value
    from the strings.json file
    """
    warnings.warn(
        'get_string is deprecated. Use "lcs" instead, or reference constants from strings directly.', DeprecationWarning
    )

    # Pull the latest changes from strings.json for faster debugging
    if env("DEBUG"):
        with open("lite_content/lite-exporter-frontend/strings.json") as json_file:
            lite_strings.constants = json.load(json_file)

    def get(d, keys):
        if "." in keys:
            key, rest = keys.split(".", 1)
            return get(d[key], rest)
        else:
            return d[keys]

    return_value = get(lite_strings.constants, value)

    if isinstance(return_value, list):
        return return_value

    return get(lite_strings.constants, value).format(*args, **kwargs)


@register.filter
@stringfilter
def str_date(value):
    return_value = do_timezone(datetime.datetime.strptime(value, ISO8601_FMT), "Europe/London")
    return (
        return_value.strftime("%-I:%M") + return_value.strftime("%p").lower() + " " + return_value.strftime("%d %B %Y")
    )


@register.filter()
def strip_underscores(value):
    value = value[0:1].upper() + value[1:]
    return value.replace("_", " ")


@register.filter
@stringfilter
def units_pluralise(unit: str, quantity: str):
    """
    Pluralise goods measurements units
    """
    if unit.endswith("(s)"):
        unit = unit[:-3]

        if not quantity == "1":
            unit = unit + "s"

    return unit


@register.filter
@stringfilter
@mark_safe
def highlight_text(value: str, term: str) -> str:
    def insert_str(string, str_to_insert, string_index):
        return string[:string_index] + str_to_insert + string[string_index:]

    if not term.strip():
        return value

    indexes = [m.start() for m in re.finditer(term, value, flags=re.IGNORECASE)]

    span = '<span class="lite-highlight">'
    span_end = "</span>"

    loop = 0
    for index in indexes:
        # Count along the number of positions of the new string then adjust for zero index
        index += loop * (len(span) + len(term) + len(span_end) - 1)
        loop += 1
        value = insert_str(value, span, index)
        value = insert_str(value, span_end, index + len(span) + len(term))

    return value


@register.filter()
def reference_code(value):
    """
    Converts ten digit string to two five digit strings hyphenated
    """
    value = str(value)
    return value[:5] + "-" + value[5:]


@register.filter
@mark_safe
def pretty_json(value):
    """
    Pretty print JSON - for development purposes only.
    """
    return "<pre>" + json.dumps(value, indent=4) + "</pre>"


@register.filter(name="times")
def times(number):
    """
    Returns a list of numbers from 1 to the number
    """
    return [x + 1 for x in range(number)]


@register.filter()
def default_na(value):
    """
    Returns N/A if the parameter given is none
    """
    if value:
        return value
    else:
        return mark_safe('<span class="lite-hint">N/A</span>')  # nosec


@register.filter()
def friendly_boolean(boolean):
    """
    Returns 'Yes' if a boolean is equal to True, else 'No'
    """
    if boolean is True or str(boolean).lower() == "true":
        return "Yes"
    else:
        return "No"


@register.filter()
def pluralise_unit(unit, value):
    """
    Modify units given from the API to include an 's' if the
    value is not singular.

    Units require an (s) at the end of their names to
    use this functionality.
    """
    is_singular = value == "1"

    if "(s)" in unit:
        if is_singular:
            return unit.replace("(s)", "")
        else:
            return unit.replace("(s)", "s")

    return unit


@register.filter()
def idify(string: str):
    """
    Converts a string to a format suitable for HTML IDs
    eg 'Add goods' becomes 'add_goods'
    """
    return string.lower().replace(" ", "_")


@register.filter
def classname(obj):
    """
    Returns object class name
    """
    return obj.__class__.__name__
