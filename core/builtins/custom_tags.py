from __future__ import division

import datetime
import json
import os
import re
from collections import Counter, OrderedDict
from importlib import import_module

import bleach
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from django import template
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.defaultfilters import stringfilter, safe, capfirst
from django.templatetags.tz import localtime
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeString

from exporter.core.constants import (
    DATE_FORMAT,
    CASE_SECTIONS,
    PAGE_DATE_FORMAT,
    STANDARD,
    OPEN,
    NOT_STARTED,
    DONE,
    IN_PROGRESS,
    PRODUCT_CATEGORY_FIREARM,
    FIREARM_AMMUNITION_COMPONENT_TYPES,
)
from exporter.applications.constants import F680

from caseworker.core.constants import SystemTeamsID, SLA_CIRCUMFERENCE, PARTY_TYPE_MAPPING


strings = import_module(settings.LITE_CONTENT_IMPORT_PATH)

register = template.Library()
STRING_NOT_FOUND_ERROR = "STRING_NOT_FOUND"


@register.filter(name="sla_colour")
def sla_colour(value, arg):
    """
    Template tag to calculate the colour of caseworker/templates/includes/sla_display.html
    """
    since_raised = int(value)

    if arg == "hours":
        if since_raised >= 48:
            return "red"
        else:
            return "orange"

    elif arg == "days":
        if since_raised >= 5:
            return "green"
        elif since_raised < 5 and since_raised > 0:
            return "orange"
        elif since_raised <= 0:
            return "red"

    else:
        raise ValueError("Please specify whether the time remaining is hours or days eg \"value|sla_colour:'hours'\"")


@register.filter(name="sla_ratio")
def sla_ratio(value, arg):
    """
    Template tag to calculate the stroke-dashoffset in caseworker/templates/includes/sla_display.html
    """

    elapsed = int(value)
    total = int(arg)

    amount = SLA_CIRCUMFERENCE - (elapsed / total * SLA_CIRCUMFERENCE)

    if amount < 0:
        return SLA_CIRCUMFERENCE

    return amount


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
            if isinstance(object, str):
                object = mark_safe(  # nosec
                    object.replace("<!--", "<span class='govuk-visually-hidden'>").replace("-->", "</span>")
                )

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
        return_value = localtime(parse(value))
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
    if value != "None":
        return localtime(parse(value)).strftime("%-d %B %Y")


@register.filter
@mark_safe
def pretty_json(value):
    """
    Pretty print JSON - for development purposes only.
    """
    return "<pre>" + json.dumps(value, indent=4) + "</pre>"


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
def friendly_boolean_or_default_na(value):
    return default_na(value) if value is None else friendly_boolean(value)


@register.filter()
def default_na(value):
    """
    Returns N/A if the parameter given is none
    """
    if value:
        return value
    else:
        return mark_safe(f'<span class="govuk-hint govuk-!-margin-0">N/A</span>')  # nosec


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


@register.filter()
def dummy_link(name=None):
    name = escape(name)

    return safe(
        f'<a href="javascript:void(0);" rel="noreferrer noopener" target="_blank" class="govuk-link govuk-link--no-visited-state">{name}</a>'
    )


@register.filter
@stringfilter
def highlight_text(value: str, term: str) -> str:
    value = escape(value)

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

    return SafeString(bleach.clean(value, tags=["mark"], attributes={"mark": ["class"]}))  # nosec


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
    return PARTY_TYPE_MAPPING[party["type"]]


@register.filter()
def is_system_team(id: str):
    ids = [team_id.value for team_id in SystemTeamsID]
    return id in ids


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
def join_key_value_list(_list, _join=", "):
    _list = [x["value"] for x in _list]
    return join_list(_list, _join)


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


@register.filter()
def subtract(num1, num2):
    if not num1:
        return 0
    if not num2:
        return num1
    return num1 - num2


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
    from caseworker.cases.helpers.advice import convert_advice_item_to_base64, order_grouped_advice

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
def filter_advice_by_user_id(advice, user_id):
    return [advice for advice in advice if advice["user"]["id"] == user_id]


@register.filter()
def filter_advice_by_team_id(advice, team_id):
    return [advice for advice in advice if advice["user"]["team"]["id"] == team_id]


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


@register.filter()
def list_has_property(items, attribute):
    for item in items:
        if attribute in item and item.get(attribute):
            return True
    return False


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
def date_display(value):
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    # ensure that the value given exists, and is not none type
    if not value:
        return

    # A date without the two '-' delimiters is not a full/valid date
    if value.count("-") < 2:
        return

    year, month, day = value.split("-")
    month = months[(int(month) - 1)]

    return f"{int(day)} {month} {year}"


@register.filter()
def add_months(start_date, months):
    """
    Return a date with an added desired number of business months
    Example 31/1/2020 + 1 month = 29/2/2020 (one business month)
    """
    start_date = datetime.datetime.strptime(start_date, DATE_FORMAT)
    new_date = start_date + relativedelta(months=+months)
    return new_date.strftime(PAGE_DATE_FORMAT)


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


def format_quantity_units(quantity):
    unit_suffix = "item"
    quantity = int(quantity) if quantity is not None else 0
    if quantity == 0 or quantity > 1:
        unit_suffix = "items"

    return f"{quantity} {unit_suffix}"


@register.filter
def pluralise_quantity(good_on_app):
    """
    Pluralise goods quantity
    """
    quantity = good_on_app.get("quantity", 0)
    unit = good_on_app.get("unit", {}).get("key")

    if good_on_app.get("good", {}).get("item_category", {}).get("key") == PRODUCT_CATEGORY_FIREARM:
        if (
            good_on_app.get("firearm_details") is not None
            and good_on_app["firearm_details"]["type"]["key"] in FIREARM_AMMUNITION_COMPONENT_TYPES
        ):
            # because these are number of articles
            return format_quantity_units(quantity)
        elif unit:
            if unit == "NAR":
                return format_quantity_units(quantity)
            return f"{quantity} {good_on_app['unit']['value']}"
        else:
            return f"{quantity} items"
    else:
        if unit and unit != "NAR":
            quantity_str = f"{intcomma(quantity)} {units_pluralise(unit, intcomma(quantity))}"
        else:
            quantity_str = f"{format_quantity_units(quantity)}"

    return quantity_str


@register.filter(name="times")
def times(number):
    """
    Returns a list of numbers from 1 to the number
    """
    return [x + 1 for x in range(number)]


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


@register.filter
def task_list_additional_information_status(data):
    """
    Returns 'not started' if length of data given is none, else returns 'done'
    """
    if all([data.get(field) in ["", None] for field in F680.REQUIRED_FIELDS]):
        return NOT_STARTED

    for field in F680.REQUIRED_FIELDS:
        if field in data:
            if data[field] is None or data[field] == "":
                return IN_PROGRESS
            if data[field] is True:
                secondary_field = F680.REQUIRED_SECONDARY_FIELDS.get(field, False)
                if secondary_field and not data.get(secondary_field):
                    return IN_PROGRESS
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
    return value.get(arg) if value else None


@register.filter()
def getitem(obj, name):
    return obj[name]


@register.filter()
def application_type_in_list(application_type, application_types):
    types = CASE_SECTIONS[application_types]
    if isinstance(types, list):
        return application_type in types
    else:
        return application_type == types


@register.filter()
def get_end_use_details_status(application):
    fields = ["intended_end_use"]
    if application.sub_type in [STANDARD, OPEN]:
        fields += ["is_military_end_use_controls", "is_informed_wmd", "is_suspected_wmd"]
        if application.sub_type == STANDARD:
            fields.append("is_eu_military")
    end_use_detail_field_data = [application.get(field) is not None for field in fields]

    if all(end_use_detail_field_data):
        return DONE
    elif any(end_use_detail_field_data):
        return IN_PROGRESS
    else:
        return NOT_STARTED


@register.filter()
def get_parties_status_optional_documents(parties):
    if not parties:
        return NOT_STARTED

    if isinstance(parties, list):
        for party in parties:
            if not party:
                return NOT_STARTED
    else:
        if not parties["documents"]:
            if parties["type"] == "end_user" and parties["end_user_document_available"] is False:
                return DONE
            return IN_PROGRESS

    return DONE


@register.filter()
def requires_ultimate_end_users(goods):
    ultimate_end_users_required = False

    for good in goods:
        if good["is_good_incorporated"]:
            ultimate_end_users_required = True

    return ultimate_end_users_required


def join_list(_list, _join=", "):
    return _join.join(_list)


@register.filter()
def abbreviate_string(string, length):
    if len(str(string)) <= length:
        return string
    else:
        return str(string)[:length] + "..."


@register.filter
def index(string, index):
    return string[index]


@register.filter()
def display_clc_ratings(control_list_entries):
    ratings = [item["rating"] for item in control_list_entries]
    return ", ".join(ratings)


def party_status(party):
    if not party:
        return NOT_STARTED

    if not party["documents"]:
        if party["type"] == "end_user" and party["end_user_document_available"] is False:
            return DONE

        return IN_PROGRESS

    return DONE


@register.filter()
def get_parties_status(parties):
    if not parties:
        return NOT_STARTED

    if isinstance(parties, list):
        for party in parties:
            return party_status(party)
    else:
        return party_status(parties)

    return DONE


@register.filter
def divide(value, other):
    try:
        return float(value) / float(other)
    except (ValueError, ZeroDivisionError, TypeError):
        return None


@register.filter
def full_name(user):
    user = user or {}
    return f"{user.get('first_name', '')} {user.get('last_name', '')}"


@register.filter
def verbose_goods_starting_point(value):
    goods_starting_points = {"GB": "Great Britain", "NI": "Northern Ireland"}
    return goods_starting_points.get(value, "")


@register.filter
def document_extension(filename):
    _, ext = os.path.splitext(filename)
    return ext[1:]
