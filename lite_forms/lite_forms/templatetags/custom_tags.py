from django.template.defaulttags import register


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
        if 'id' in data:
            return data['id'] == key
        if 'key' in data:
            return data['key'] == key

    # If data is a list, check for the key
    if isinstance(data, list):
        if key in data:
            return True

        for item in data:
            if isinstance(item, str):
                if item == key:
                    return True
            else:
                if item.get('id') == key:
                    return True

    return False


@register.filter
def prefix_dots(text):
    return text.replace('.', '\\\.')
