import datetime
import json

import stringcase
from django import template
from django.template.defaultfilters import stringfilter
from django.templatetags.tz import do_timezone
from django.utils.safestring import mark_safe

from conf.constants import ISO8601_FMT
from conf.settings import env
from core import strings

register = template.Library()


@register.simple_tag
def get_string(value):
    """
    Given a string, such as 'cases.manage.attach_documents' it will return the relevant value
    from the strings.json file
    """

    # Pull the latest changes from strings.json for faster debugging
    if env('DEBUG'):
        with open('lite-content/lite-internal-frontend/strings.json') as json_file:
            strings.constants = json.load(json_file)

    def get(d, keys):
        if "." in keys:
            key, rest = keys.split(".", 1)
            return get(d[key], rest)
        else:
            return d[keys]

    return get(strings.constants, value)


@register.filter
@stringfilter
def str_date(value):
    return_value = do_timezone(datetime.datetime.strptime(value, ISO8601_FMT), 'Europe/London')
    return return_value.strftime('%-I:%M') + return_value.strftime('%p').lower() + ' ' + return_value.strftime('%d %B '
                                                                                                               '%Y')


@register.filter()
def sentence_case(value):
    return stringcase.sentencecase(value)


@register.filter()
def add_selected_class(key, url):
    if key in url:
        return 'lite-menu-item--selected'

    return ''


@register.filter()
def table_sort(key, actual_sort):
    actual_sort = actual_sort.get('sort')

    if not actual_sort:
        return ''

    if actual_sort == key:
        return 'lite-cases-table__heading--active'

    if '-' + key in actual_sort:
        return 'lite-cases-table__heading--active-desc'


@register.filter()
def table_sort_text(key, actual_sort):
    actual_sort = actual_sort.get('sort')

    if not actual_sort:
        return key

    if '-' + key in actual_sort:
        return ''

    if key in actual_sort:
        return '-' + key


@register.filter()
def add_subnav_selected_class(key, url):
    if key in url:
        return 'lite-subnav__link--selected'

    return ''


@register.filter()
def group_list(items, split):
    """
    Groups items in a list based on a specified size
    """
    return [items[x:x+split] for x in range(0, len(items), split)]


@register.filter
@mark_safe
def pretty_json(value):
    """
    Pretty print JSON - for development purposes only.
    """
    return '<pre>' + json.dumps(value, indent=4) + '</pre>'


@register.filter(name='times')
def times(number):
    return [x+1 for x in range(number)]
