from django.template.defaulttags import register


@register.filter(name='keyvalue')
def keyvalue(dictionary, key):
    if not dictionary:
        return
    return dictionary.get(key)


@register.filter(name='pluralise_unit')
def pluralise_unit(unit, value):
    is_singular = value == '1'

    if '(s)' in unit:
        if is_singular:
            return unit.replace('(s)', '')
        else:
            return unit.replace('(s)', 's')

    return unit
