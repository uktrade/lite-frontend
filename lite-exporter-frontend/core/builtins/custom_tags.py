from django import template
from django.template.defaultfilters import stringfilter

import datetime
import stringcase

from conf.constants import ISO8601_FMT
from core import strings

register = template.Library()


@register.simple_tag
def get_string(value):

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
    return datetime.datetime.strptime(value, ISO8601_FMT)


@register.filter()
def sentence_case(value):
    return stringcase.sentencecase(value)
