from django.template.defaulttags import register


@register.filter(name='keyvalue')
def keyvalue(dictionary, key):
    if not dictionary:
        return
    return dictionary.get(key)
