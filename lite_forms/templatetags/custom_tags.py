from django.template.defaulttags import register


@register.filter
def key_value(dictionary, key):
    if not dictionary:
        return
    return dictionary.get(key)


@register.filter
def key_value_split(dictionary, key):
    if '.' in key:
        split = key.split('.')
        key = split[len(split) - 1]
    if not dictionary:
        return
    return dictionary.get(key)
