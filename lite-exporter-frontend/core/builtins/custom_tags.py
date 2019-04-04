from django import template
from django.template.defaultfilters import stringfilter

from conf import strings
import datetime

from conf.constants import ISO8601_FMT

register = template.Library()


@register.simple_tag
def get_string(value):
    return strings.constants[value]


@register.filter
@stringfilter
def str_date(value):
    return datetime.datetime.strptime(value, ISO8601_FMT)
