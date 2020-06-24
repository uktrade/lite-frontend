from __future__ import division

import datetime
import json
import math
import re
from collections import Counter, OrderedDict
from html import escape

from django import template
from django.template.defaultfilters import stringfilter, safe, capfirst
from django.templatetags.tz import do_timezone
from django.utils.safestring import mark_safe

from conf import settings
from conf.constants import ISO8601_FMT, DATE_FORMAT
from conf.constants import SystemTeamsID, CaseType
from lite_content.lite_internal_frontend import strings

register = template.Library()
STRING_NOT_FOUND_ERROR = "STRING_NOT_FOUND"


@register.simple_tag(name="lcs")
@mark_safe
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
            return object.replace("<!--", "<span class='govuk-visually-hidden'>").replace("-->", "</span>")
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


@register.filter(name="lcsp")
def pluralize_lcs(items, string):
    """
    Given a list of items and an LCS string, return the singular version if the list
    contains one item otherwise return the plural version
    {{ open_general_licence.control_list_entries|lcsp:'open_general_licences.List.Table.CONTROL_LIST_ENTRIES' }}
    CONTROL_LIST_ENTRIES = "Control list entry/Control list entries"
    """
    strings = get_const_string(string).split("/")
    count = items if isinstance(items, int) else len(items) if items else 0

    if count == 1:
        return strings[0]
    else:
        return strings[1]


@register.filter
@stringfilter
def str_date(value):
    try:
        return_value = do_timezone(datetime.datetime.strptime(value, ISO8601_FMT), "Europe/London")
        return (
            return_value.strftime("%-I:%M")
            + return_value.strftime("%p").lower()
            + " "
            + return_value.strftime("%d %B " "%Y")
        )
    except ValueError:
        return


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
def friendly_boolean_or_default_na(value):
    return default_na(value) if value is None else friendly_boolean(value)


@register.filter()
def default_na(value):
    """
    Returns N/A if the parameter given is none
    """
    if value is not None and len(value):
        return value
    else:
        return mark_safe(f'<span class="govuk-hint govuk-!-margin-0">{strings.NOT_APPLICABLE}</span>')  # nosec


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
        country = data.get("country")

        if "country" in address:
            country = address.get("country")

        if isinstance(address, str):
            if country:
                return address + ", " + country["name"]
            else:
                return address

        if "address_line_1" in address:
            address = [
                address["address_line_1"],
                address["address_line_2"],
                address["city"],
                address["region"],
                address["postcode"],
            ]
        else:
            address = [
                address["address"],
            ]

        if country:
            address.append(country["name"])

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

    return safe(
        f'<a href="{address}" rel="noreferrer noopener" target="_blank" class="govuk-link govuk-link--no-visited-state">{name} '
        f'<span class="govuk-visually-hidden">(opens in new tab)</span></a>'
    )


@register.filter
@stringfilter
@mark_safe
def highlight_text(value: str, term: str) -> str:
    def insert_str(string, str_to_insert, string_index):
        return string[:string_index] + str_to_insert + string[string_index:]

    if not term or not term.strip():
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
    remaining_days = case["sla_remaining_days"]

    if remaining_days <= 0:
        return "100"
    else:
        return _round_percentage((case["sla_days"] / (case["sla_days"] + case["sla_remaining_days"])) * 100)


@register.filter()
def get_sla_hours_percentage(case):
    sla_hours_since_raised = case["sla_hours_since_raised"]
    return _round_percentage((sla_hours_since_raised / 48) * 100)


def _round_percentage(percentage):
    # Round up to nearest 10
    if percentage == 0:
        return "10"
    elif percentage >= 100:
        return "100"
    else:
        return str(math.ceil(percentage / 10) * 10)


@register.filter()
def get_sla_ring_colour(case):
    remaining_days = case["sla_remaining_days"]

    if remaining_days > 5:
        return "green"
    elif remaining_days >= 0:
        return "yellow"
    else:
        return "red"


@register.filter()
def get_sla_hours_ring_colour(case):
    sla_hours_since_raised = case["sla_hours_since_raised"]

    if sla_hours_since_raised >= 48:
        return "red"
    else:
        return "yellow"


@register.filter()
def is_exhibition(case_type):
    return case_type == CaseType.EXHIBITION


@register.filter()
def is_f680(case_type):
    return case_type == CaseType.F680


@register.simple_tag
@mark_safe
def missing_title():
    """
    Adds a missing title banner to the page
    """
    if not settings.DEBUG:
        return

    return (
        "</title>"
        "</head>"
        '<body style="margin-top: 73px;">'
        '<div class="app-missing-title-banner">'
        '<div class="govuk-width-container">'
        '<h2 class="app-missing-title-banner__heading">You need to set a title!</h2>'
        'You can do this by adding <span class="app-missing-title-banner__code">{% block title %}'
        '<span class="app-missing-title-banner__code--tint">My first title!</span>{% endblock %}</span> to your HTML'
        "</div>"
        "</div>"
    )


@register.filter()
def equals(ob1, ob2):
    return ob1 == ob2


@register.filter()
def not_equals(ob1, ob2):
    return ob1 != ob2


@register.filter()
@mark_safe
def aurora(flags):
    """
    Generates a radial gradient background from a list of flags
    """
    colours = {
        "default": "#626a6e",
        "red": "#d4351c",
        "orange": "#f47738",
        "blue": "#1d70b8",
        "yellow": "#FED90C",
        "green": "#00703c",
        "pink": "#d53880",
        "purple": "#4c2c92",
        "brown": "#b58840",
        "turquoise": "#28a197",
    }

    bucket = [colours[flag["colour"]] for flag in flags]

    if len(set(bucket)) != len(bucket):
        bucket = list(OrderedDict.fromkeys(item for items, c in Counter(bucket).most_common() for item in [items] * c))

    if not bucket:
        return

    while len(bucket) < 4:
        bucket.extend(bucket)

    gradients = [
        f"radial-gradient(ellipse at top left, {bucket[0]}, transparent)",
        f"radial-gradient(ellipse at top right, {bucket[1]}, transparent)",
        f"radial-gradient(ellipse at bottom left, {bucket[2]}, transparent)",
        f"radial-gradient(ellipse at bottom right, {bucket[3]}, transparent)",
    ]

    return 'style="background: ' + ",".join(gradients) + '"'


@register.filter()
def multiply(num1, num2):
    if not num1:
        return 0
    return float(num1) * float(num2)


def join_list(_list, _join=", "):
    return _join.join(_list)


@register.filter()
def join_key_value_list(_list, _join=", "):
    _list = [x["value"] for x in _list]
    return join_list(_list, _join)


@register.filter()
def filter_advice_by_user(advice, id):
    return_list = []

    for advice in advice:
        if advice["user"]["id"] == id:
            return_list.append(advice)

    return return_list


@register.filter()
def filter_advice_by_id(advice, id):
    return_list = []

    for advice in advice:
        for key in ["good", "goods_type", "country", "end_user", "ultimate_end_user", "consignee", "third_party"]:
            if key in advice and advice[key] == id:
                return_list.append(advice)

    return return_list


@register.filter()
def distinct_advice(advice_list, case):
    from cases.helpers.advice import convert_advice_item_to_base64, order_grouped_advice

    return_value = {}

    for advice_item in advice_list:
        # Goods
        advice_item["token"] = convert_advice_item_to_base64(advice_item)

        good = advice_item.get("good") or advice_item.get("goods_type")
        case_good = None
        for item in case.goods:
            if "good" in item:
                if item["good"]["id"] == good:
                    case_good = item
            else:
                if item["id"] == good:
                    case_good = item

        # Destinations
        destination_fields = [
            advice_item.get("ultimate_end_user"),
            advice_item.get("country"),
            advice_item.get("third_party"),
            advice_item.get("end_user"),
            advice_item.get("consignee"),
        ]
        destination = next((destination for destination in destination_fields if destination), None)
        case_destination = next(
            (case_destination for case_destination in case.destinations if case_destination["id"] == destination), None
        )

        if not advice_item["token"] in return_value:
            advice_item["goods"] = []
            advice_item["destinations"] = []
            return_value[advice_item["token"]] = advice_item

        if case_good:
            return_value[advice_item["token"]]["goods"].append(case_good)
        if case_destination:
            return_value[advice_item["token"]]["destinations"].append(case_destination)

    # Add goods/destinations that have no advice
    no_advice_goods = []
    no_advice_destinations = []

    for good in case.goods:
        if not filter_advice_by_id(advice_list, good.get("good", good).get("id")):
            no_advice_goods.append(good)

    for destination in case.destinations:
        if not filter_advice_by_id(advice_list, destination["id"]):
            no_advice_destinations.append(destination)

    if no_advice_goods or no_advice_destinations:
        return_value["no_advice"] = {
            "id": "no_advice",
            "type": {"key": "no_advice", "value": "No advice"},
            "goods": no_advice_goods,
            "destinations": no_advice_destinations,
        }

    return order_grouped_advice(return_value)


@register.filter()
def values(dictionary):
    return dictionary.values()


@register.filter()
def filter_advice_by_level(advice, level):
    return [advice for advice in advice if advice["level"] == level]


@register.filter()
def sentence_case(text):
    return capfirst(text).replace("_", " ")


@register.filter()
def format_heading(text):
    return text.replace("_", " ")


@register.filter()
def goods_value(goods):
    total_value = 0

    for good in goods:
        total_value += float(good.get("value", 0))

    return total_value


@register.filter()
def latest_status_change(activity):
    return next((item for item in activity if "updated the status" in item["text"]), None)


@register.filter()
def filter_flags_by_level(flags, level):
    return [flag for flag in flags if flag["level"] == level]


@register.filter()
def get_goods_linked_to_destination_as_list(goods, country_id):
    """
    Instead of iterating over each goods list of countries without the ability to break loops in django templating.
    This function will make a match for which goods are being exported to the country supplied,
        and return the list of goods
    :param goods: list of goods on the application
    :param country_id: id of country we are interested in
    :return: list of goods that go to destination
    """
    item_number = 1
    list_of_goods = []
    for good in goods:
        for country in good["countries"]:
            if country["id"] == country_id:
                list_of_goods.append(f"{item_number}. {good['description']}")
                item_number += 1
                break
        else:
            break

    return list_of_goods
