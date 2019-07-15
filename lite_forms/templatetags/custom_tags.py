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

        return key in array

    # If else, loop through and check ids
    return key in [x.get('id') for x in array]


@register.filter
def prefix_dots(text):
    return text.replace('.', '\\\.')
