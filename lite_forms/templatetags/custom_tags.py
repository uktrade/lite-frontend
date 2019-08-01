from django.template.defaulttags import register


@register.filter
def key_value(dictionary, key):
    if not dictionary:
        return
    return dictionary.get(key)


@register.filter
def key_in_array(data, key):
    # If data is empty, return False
    if not data:
        return False

    if isinstance(data, str):
        if data == key:
            return True
        return False

    if isinstance(data, bool):
        return data

    # If data is a dict, check the id
    if isinstance(data, dict):
        if 'id' in data:
            return data['id'] == key
        if 'key' in data:
            return data['key'] == key

    # If data is a list, check for the key
    if isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                return item == key

            if item.get('id') == key:
                return True

        return key in data

    # If else, loop through and check ids
    return key in [x.get('id') for x in data]


@register.filter
def prefix_dots(text):
    return text.replace('.', '\\\.')
