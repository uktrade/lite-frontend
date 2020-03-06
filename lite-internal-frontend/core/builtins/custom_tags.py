from __future__ import division

import datetime
import json
import math
import re
import warnings
from html import escape

from django import template
from django.template.defaultfilters import stringfilter, safe
from django.templatetags.tz import do_timezone
from django.utils.safestring import mark_safe

from conf.constants import ISO8601_FMT, DATE_FORMAT

from lite_content.lite_internal_frontend import strings
from conf.constants import SystemTeamsID, CaseType

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

    warnings.warn("Reference constants from strings directly, only use LCS in HTML files", Warning)
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
        return_value.strftime("%-I:%M")
        + return_value.strftime("%p").lower()
        + " "
        + return_value.strftime("%d %B " "%Y")
    )


@register.filter
@stringfilter
def str_date_only(value):
    date_str = do_timezone(datetime.datetime.strptime(value, DATE_FORMAT), "Europe/London")
    return date_str.strftime("%d %B %Y")


@register.filter()
def reference_code(value):
    value = str(value)
    return value[:5] + "-" + value[5:]


@register.filter()
def add_selected_class(key, url):
    if key == url:
        return "lite-menu-item--selected"

    return ""


@register.filter()
def table_sort(key, actual_sort):
    actual_sort = actual_sort.get("sort")

    if not actual_sort:
        return ""

    if actual_sort == key:
        return "lite-cases-table__heading--active"

    if "-" + key in actual_sort:
        return "lite-cases-table__heading--active-desc"


@register.filter()
def table_sort_text(key, actual_sort):
    actual_sort = actual_sort.get("sort")

    if not actual_sort:
        return key

    if "-" + key in actual_sort:
        return ""

    if key in actual_sort:
        return "-" + key


@register.filter()
def add_subnav_selected_class(key, url):
    if key in url:
        return "lite-subnav__link--selected"

    return ""


@register.filter()
def group_list(items, split):
    """
    Groups items in a list based on a specified size
    """
    return [items[x : x + split] for x in range(0, len(items), split)]


@register.filter
@mark_safe
def pretty_json(value):
    """
    Pretty print JSON - for development purposes only.
    """
    return "<pre>" + json.dumps(value, indent=4) + "</pre>"


@register.filter(name="times")
def times(number):
    return [x + 1 for x in range(number)]


def replace_all(text, old, new):
    while old in text:
        text = text.replace(old, new)
    return text


@register.filter(name="old_character")
def old_character(text, old_char):
    return replace_all(text, old_char, "$$")


@register.filter(name="new_character")
def new_character(text, new_char):
    return replace_all(text, "$$", new_char)


@register.simple_tag
@mark_safe
def hidden_field(key, value):
    """
    Generates a hidden field from the given key and value
    """
    return f'<input type="hidden" name="{key}" value="{value}">'


@register.filter()
def friendly_boolean(boolean):
    """
    Returns 'Yes' if a boolean is equal to True, else 'No'
    """
    if boolean is True or boolean == "true" or boolean == "True" or boolean == "yes" or boolean == "Yes":
        return "Yes"
    else:
        return "No"


@register.filter()
def get_first_country_from_first_good(dictionary: dict):
    """
    Returns the first key in a dictionary
    """
    return list(dictionary)[0] + "." + next(iter(dictionary.values()))[0]


@register.filter()
def get_end_user(application: dict):
    if application.get("end_user"):
        return application.get("end_user")
    return application.get("destinations").get("data")


@register.filter()
def default_na(value):
    """
    Returns N/A if the parameter given is none
    """
    if value:
        return value
    else:
        return mark_safe(f'<span class="lite-hint">{strings.NOT_APPLICABLE}</span>')  # nosec


@register.filter()
def get_address(data):
    """
    Returns a correctly formatted address
    such as 10 Downing St, London, Westminster, SW1A 2AA, United Kingdom
    from {'address': {'address_line_1': '10 Downing St', ...}
    or {'address': '10 Downing St ...', 'country': {'name': United Kingdom'}}
    """
    if data and "address" in data:
        address = data["address"]

        if isinstance(address, str):
            return address + ", " + data["country"]["name"]

        address = [
            address["address_line_1"],
            address["address_line_2"],
            address["city"],
            address["region"],
            address["postcode"],
            address["country"]["name"],
        ]
        return ", ".join([x for x in address if x])
    return ""


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


@register.filter
@stringfilter
@mark_safe
def highlight_text(value: str, term: str) -> str:
    def insert_str(string, str_to_insert, string_index):
        return string[:string_index] + str_to_insert + string[string_index:]

    if not term.strip():
        return value

    indexes = [m.start() for m in re.finditer(term, value, flags=re.IGNORECASE)]

    mark_start = '<mark class="lite-highlight">'
    mark_end = "</mark>"

    loop = 0
    for index in indexes:
        # Count along the number of positions of the new string then adjust for zero index
        index += loop * (len(mark_start) + len(term) + len(mark_end) - 1)
        loop += 1
        value = insert_str(value, mark_start, index)
        value = insert_str(value, mark_end, index + len(mark_start) + len(term))

    return value


@register.filter()
def username(user: dict):
    """
    Returns the user's first and last name if they've seen set, else
    returns the user's email
    """
    if user["first_name"]:
        return user["first_name"] + " " + user["last_name"]

    return user["email"]


@register.filter()
def get_party_type(party):
    return {
        "end_user": "End User",
        "third_party": "Third Party",
        "ultimate_end_user": "Ultimate End User",
        "consignee": "Consignee",
    }[party["type"]]


@register.filter()
def display_grading(text: str):
    value = text.split("_")
    if len(value):
        return f"{value[0].upper()} {' '.join(value[1:]).title()}"

    return text


@register.filter()
def is_system_team(id: str):
    ids = [team_id.value for team_id in SystemTeamsID]
    return id in ids


@register.filter()
def get_sla_percentage(case):
    if case["sla_remaining_days"] <= 0:
        return "100"
    else:
        percentage = (case["sla_days"] / (case["sla_days"] + case["sla_remaining_days"])) * 100
        # Round up to nearest 10
        if percentage == 0:
            return "10"
        else:
            percentage = math.ceil(percentage / 10) * 10
            return str(percentage)


@register.filter()
def get_sla_ring_colour(remaining_days):
    if remaining_days > 5:
        return "green"
    elif remaining_days >= 0:
        return "yellow"
    else:
        return "red"


@register.filter()
def is_exhibition(case_type):
    result = True if case_type == CaseType.EXHIBITION else False
    return result
