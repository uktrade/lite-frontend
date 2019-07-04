from django.template.defaulttags import register


@register.filter
def key_value(dictionary, key):
    if not dictionary:
        return
    return dictionary.get(key)


@register.filter
def key_in_array(array, key):
    # If array is empty, return False
    if not array:
        return False

    # If array is a list, check for the key
    if isinstance(array, list):
        for item in array:
            if isinstance(item, str):
                return item == key

            if item.get('id') == key:
                return True

        if key in array:
            return True
        return False

    # If else, loop through
    for item in array:
        if item.get('id') == key:
            return True
    return False


@register.filter
def id_in_array(array, key):
    # If array is empty, return False
    if not array:
        return False

    # If else, loop through
    for item in array:
        if item.get('id') == key:
            return True
    return False


@register.filter
def prefix_dots(text):
    return text.replace('.', '\\\.')
