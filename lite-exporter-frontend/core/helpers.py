import datetime
from collections import defaultdict
from html import escape

from django.template.defaultfilters import safe
from django.templatetags.tz import do_timezone

from conf.constants import ISO8601_FMT
from core.builtins.custom_tags import default_na


class Section:
    def __init__(self, title, tiles):
        self.title = title
        self.tiles = tiles


class Tile:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url


def str_to_bool(v, invert_none=False):
    if v is None:
        return invert_none
    if isinstance(v, bool):
        return v
    return v.lower() in ("yes", "true", "t", "1")


def str_date_only(value):
    return_value = do_timezone(datetime.datetime.strptime(value, ISO8601_FMT), "Europe/London")
    return return_value.strftime("%d %B %Y")


def generate_notification_string(notifications, object_type):
    notifications_count = len(
        [x for x in notifications if x["object_type"] == object_type or x["parent_type"] == object_type]
    )

    if notifications_count == 0:
        return ""
    elif notifications_count == 1:
        return f"You have {notifications_count} new notification"
    else:
        return f"You have {notifications_count} new notifications"


def group_notifications(notifications: list):
    """
    Groups and counts notifications by object and parent ID
    """
    notifications_filtered = defaultdict(int)

    for notification in notifications:
        notifications_filtered[notification["object"]] += 1
        notifications_filtered[notification["parent"]] += 1

    return notifications_filtered


def convert_value_to_query_param(key: str, value):
    """
    Convert key/value pairs to a string suitable for query parameters
    eg {'type': 'organisation'} becomes type=organisation
    eg {'type': ['organisation', 'organisation']} becomes type=organisation&type=organisation
    """
    if isinstance(value, list):
        return_value = ""
        for item in value:
            if not return_value:
                return_value = return_value + key + "=" + item
            else:
                return_value = return_value + "&" + key + "=" + item
        return return_value

    return key + "=" + str(value)


def convert_dict_to_query_params(dictionary: dict):
    return "&".join(([convert_value_to_query_param(key, value) for (key, value) in dictionary.items()]))


def convert_parameters_to_query_params(dictionary: dict):
    """
    Given a dictionary of parameters, convert to a query param string
    Removes request object and deletes empty keys
    """
    if "request" in dictionary:
        del dictionary["request"]

    return "?" + convert_dict_to_query_params({key: value for key, value in dictionary.items() if value is not None})


def convert_to_link(address, name=None, classes="", include_br=False):
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

    br = "<br>" if include_br else ""

    return safe(f'<a href="{address}" class="govuk-link govuk-link--no-visited-state {classes}">{name}</a>{br}')


def remove_prefix(json, prefix):
    post_data = {}
    for k in json:
        if k.startswith(prefix):
            field = k[len(prefix) :]
            post_data[field] = json[k]
    return post_data


def println(content=None, no=1):
    print("\n" * no)
    if content:
        print(content)
        print("\n" * no)
