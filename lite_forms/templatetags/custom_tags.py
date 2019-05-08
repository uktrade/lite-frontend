from django.template.defaulttags import register


@register.filter
def key_value(dictionary, key):
    if not dictionary:
        return
    return dictionary.get(key)


@register.filter
def prefix_dots(text):
    return text.replace('.', '\\\.')
