import datetime
import json
import re
from html import escape

from django import template
from django.template.defaultfilters import stringfilter, safe
from django.templatetags.tz import do_timezone
from django.utils.safestring import mark_safe

from conf.constants import ISO8601_FMT, NOT_STARTED, DONE

from lite_content.lite_exporter_frontend import strings

register = template.Library()
STRING_NOT_FOUND_ERROR = "STRING_NOT_FOUND"


@register.simple_tag(name="lcs")
def get_const_string(value):
    """
    Template tag for accessing constants from LITE content library (not for Python use - only HTML)
    """

    def get(object_to_search, nested_properties_list):
        """
        Recursive function used to search an unknown number of nested objects
        for a property. For example if we had a path 'cases.CasePage.title' this function
        would take the current object `object_to_search` and get an object called 'CasePage'.
        It would then call itself again to search the 'CasePage' for a property called 'title'.
        :param object_to_search: An unknown object to get the given property from
        :param nested_properties_list: The path list to the attribute we want
        :return: The attribute in the given object for the given path
        """
        object = getattr(object_to_search, nested_properties_list[0])
        if len(nested_properties_list) == 1:
            # We have reached the end of the path and now have the string
            return object
        else:
            # Search the object for the next property in `nested_properties_list`
            return get(object, nested_properties_list[1:])

    path = value.split(".")
    try:
        # Get initial object from strings.py (may return AttributeError)
        path_object = getattr(strings, path[0])
        return get(path_object, path[1:]) if len(path) > 1 else path_object
    except AttributeError:
        return STRING_NOT_FOUND_ERROR


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

    span = '<mark class="lite-highlight">'
    span_end = "</mark>"

    loop = 0
    for index in indexes:
        # Count along the number of positions of the new string then adjust for zero index
        index += loop * (len(span) + len(term) + len(span_end) - 1)
        loop += 1
        value = insert_str(value, span, index)
        value = insert_str(value, span_end, index + len(span) + len(term))

    return value


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
def linkify(address, name=None):
    """
    Returns a correctly formatted, safe link to an address
    Returns default_na if no address is provided
    """
    if not address:
        return default_na(None)

    if not name:
        name = address

    address = escape(address)
    name = escape(name)

    return safe(f'<a href="{address}" class="govuk-link govuk-link--no-visited-state">{name}</a>')


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


@register.filter
def task_list_item_status(data):
    """
    Returns 'not started' if length of data given is none, else returns 'done'
    """
    if not data:
        return NOT_STARTED

    return DONE


@register.simple_tag(name="tld")
def task_list_item_list_description(data, singular, plural):
    """
    Returns a description for a task list item depending on how many
    items are in its contents
    """
    if len(data) == 0:
        return None
    elif len(data) == 1:
        return f"1 {singular} added"
    else:
        return f"{len(data)} {plural} added"


@register.filter()
def set_lcs_variable(value, arg):
    try:
        return value % arg
    except TypeError:
        return value


@register.filter()
def get(value, arg):
    return value.get(arg)
