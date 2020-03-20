from django.template.defaulttags import register
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.builtins.custom_tags import get_const_string
from lite_forms.helpers import convert_to_markdown, flatten_data


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

    return dictionary.get(key)


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


@register.simple_tag
@mark_safe
def hidden_field(key, value):
    """
    Generates a hidden field from the given key and value
    """
    return f'<input type="hidden" name="{key}" value="{value}">'


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
    return value.get(arg, "")


@register.filter
@mark_safe
def markdown(text):
    return convert_to_markdown(text)


@register.filter
def heading_class(text):
    if text and len(text) < 150:
        return "govuk-fieldset__legend--xl"

    return "govuk-fieldset__legend--l"


@register.simple_tag
@mark_safe
def govuk_link_button(text, url, url_param=None, id="", classes=""):
    text = get_const_string(text)
    url = reverse(url, args=[url_param] if url_param else [])
    id = f'id="button-{id}"' if id else ""

    return f'<a {id} href="{url}" role="button" draggable="false" class="govuk-button {classes}" data-module="govuk-button">{text}</a>'
