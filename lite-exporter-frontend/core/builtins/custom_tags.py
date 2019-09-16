import datetime
import json
import re

from django import template
from django.template.defaultfilters import stringfilter
from django.templatetags.tz import do_timezone
from django.utils.safestring import mark_safe

from conf.constants import ISO8601_FMT
from conf.settings import env
from core import strings

register = template.Library()


@register.simple_tag
def get_string(value, *args, **kwargs):
    """
    Given a string, such as 'cases.manage.attach_documents' it will return the relevant value
    from the strings.json file
    """

    # Pull the latest changes from strings.json for faster debugging
    if env('DEBUG'):
        with open('lite-content/lite-exporter-frontend/strings.json') as json_file:
            strings.constants = json.load(json_file)

    def get(d, keys):
        if "." in keys:
            key, rest = keys.split(".", 1)
            return get(d[key], rest)
        else:
            return d[keys]

    return_value = get(strings.constants, value)

    if isinstance(return_value, list):
        return return_value

    return get(strings.constants, value).format(*args, **kwargs)


@register.filter
@stringfilter
def str_date(value):
    return_value = do_timezone(datetime.datetime.strptime(value, ISO8601_FMT), 'Europe/London')
    return return_value.strftime('%-I:%M') + return_value.strftime('%p').lower() + ' ' + return_value.strftime('%d %B %Y')


@register.filter
@stringfilter
def units_pluralise(unit: str, quantity: str):
    """
    Pluralise goods measurements units
    """
    if unit.endswith('(s)'):
        unit = unit[:-3]

        if not quantity == '1':
            unit = unit + 's'

    return unit


@register.filter
@stringfilter
@mark_safe
def highlight_text(value: str, term: str) -> str:

    def insert_str(string, str_to_insert, string_index):
        return string[:string_index] + str_to_insert + string[string_index:]

    if not term.strip():
        return value

    indexes = [m.start() for m in re.finditer(term, value, flags=re.IGNORECASE)]

    span = '<span class="lite-filter-highlight">'
    span_end = '</span>'

    for index in indexes:
        value = insert_str(value, span, index)
        value = insert_str(value, span_end, index + len(span) + len(term))

    return value


@register.filter()
def reference_code(value):
    value = str(value)
    return value[:5] + '-' + value[5:]


@register.filter
@mark_safe
def pretty_json(value):
    """
    Pretty print JSON - for development purposes only.
    """
    return '<pre>' + json.dumps(value, indent=4) + '</pre>'
