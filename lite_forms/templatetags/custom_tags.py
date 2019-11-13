from django.template.defaulttags import register
from django.utils.safestring import mark_safe


@register.filter
def key_value(dictionary, key):
    if not dictionary:
        return
    return dictionary.get(key)


@register.filter
def key_in_array(data, key):
    if not data:
        return False

    if isinstance(data, str):
        if key == data:
            return True
        return False

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
