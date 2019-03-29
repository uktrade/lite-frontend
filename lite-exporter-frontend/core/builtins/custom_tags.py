from django import template

from conf import strings

register = template.Library()


@register.simple_tag
def get_string(value):
    return strings.constants.get(value, 'COULDN\'T FIND STRING')
