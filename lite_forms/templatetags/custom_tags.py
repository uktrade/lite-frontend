import json
from html import escape
from json import JSONDecodeError

from django.template.defaulttags import register
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.builtins.custom_tags import get_const_string
from lite_forms.helpers import flatten_data


@register.filter
def has_attribute(_object, attribute):
    return hasattr(_object, attribute)


@register.filter
def component_name(data, _object):
    name = getattr(_object, "name", None)
    return flatten_data(data).get(name)


@register.filter
def key_value(dictionary, key):
    if not dictionary:
        return

    try:
        if key.endswith("[]"):
            key = key[:-2]
    # This allows defaultdicts to pass through unaffected as their keys
    # do not have the endswith attribute
    except AttributeError:
        pass

    value = dictionary.get(key)

    try:
        if isinstance(value, str):
            value = json.loads(value)
    except JSONDecodeError:
        pass

    return value


@register.filter
def has_components(component_options):
    for item in component_options:
        if getattr(item, "components", None):
            return True


@register.filter
def key_in_array(data, key):
    if data is None:
        return False

    if isinstance(data, str):
        if str(key) == data:
            return True
        return False

    if isinstance(data, bool) and isinstance(key, bool):
        return data == key

    if isinstance(data, bool):
        return data

    # If data is a dict, check the id
    if isinstance(data, dict):
        if "id" in data:
            return data["id"] == key
        if "key" in data:
            return data["key"] == key

    # If data is a list, check for the key
    if isinstance(data, list):
        if key in data:
            return True

        for item in data:
            if isinstance(item, str):
                if item == key:
                    return True
            else:
                if item.get("id") == key:
                    return True

    return False


@register.filter
def prefix_dots(text):
    """
    Prefix dots in an ID so it can be used in a jQuery selector.

    See https://stackoverflow.com/a/9930611
    """
    return text.replace(".", r"\\.")


@register.filter
def replace_spaces(text):
    """
    Replace spaces with a dash.
    """
    if not isinstance(text, str):
        return text

    return text.replace(" ", "-")


@register.simple_tag
@mark_safe  # noqa: S308
def dict_hidden_field(key, value):
    """
    Generates a hidden field from the given key and value
    """
    if isinstance(value, dict):
        value = json.dumps(value)
    if isinstance(value, list):
        unique_values = set(value)
        final_str = ""
        for item in unique_values:
            final_str += f"<input type='hidden' name='{key}[]' value='{escape(str(item))}'>"
        return final_str
    return f"<input type='hidden' name='{key}' value='{escape(str(value))}'>"


@register.filter
def classname(obj):
    """
    Returns object class name
    """
    return obj.__class__.__name__


@register.filter
def date_join(data, prefix):
    if data:
        date = dict()
        prefix_length = len(prefix)
        for key, value in data.items():
            if value and prefix in key:
                string = key[prefix_length:]
                if string == "day":
                    date["day"] = value
                elif string == "month":
                    date["month"] = value
                elif string == "year":
                    date["year"] = value
        return date


@register.filter
def get(value, arg):
    return value.get(arg, "") if value else None


@register.filter
def heading_class(text):
    if text and len(text) < 150:
        return "govuk-fieldset__legend--xl"

    return "govuk-fieldset__legend--l"


@register.filter
def file_type(file_name):
    """
    Returns the file type from a complete file name
    If the file doesn't have a file type, return "file"
    """
    if "." not in file_name:
        return "file"

    return file_name.split(".")[-1]


@register.simple_tag
def make_list(*args):
    return args


@register.filter()
def item_with_rating_exists(items, rating):
    if not items:
        return

    for item in items:
        if isinstance(item, str):
            if item == rating:
                return True

        if isinstance(item, dict):
            if item["rating"] == rating:
                return True


@register.simple_tag
@mark_safe  # noqa: S308
def govuk_link_button(text, url, url_param=None, id="", classes="", query_params="", show_chevron=False, hidden=False):
    text = get_const_string(text)
    if isinstance(url_param, str):
        url_param = [url_param]
    url = reverse(url, args=url_param if url_param else [])
    id = f'id="button-{id}"' if id else ""
    chevron = ""
    if show_chevron:
        chevron = (
            '<svg class="govuk-button__start-icon" xmlns="http://www.w3.org/2000/svg" width="13" height="15" '
            'viewBox="0 0 33 43" aria-hidden="true" focusable="false">'
            '<path fill="currentColor" d="M0 0h13l20 20-20 20H0l20-20z" /></svg>'
        )
    hidden = 'style="display: none;"' if hidden else ""

    return (
        f'<a {id} href="{url}{query_params}" role="button" draggable="false" class="govuk-button {classes}" {hidden} '
        f'data-module="govuk-button">{text}{chevron}</a>'
    )


@register.filter()
def unique_list(items):
    new_items = []
    for item in items:
        if item not in new_items:
            new_items.append(item)
    return new_items
