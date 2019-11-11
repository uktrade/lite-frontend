import re

import bleach
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

OPEN_TAG = '<span class="lite-highlight">'
ALT_OPEN_TAG = '<span class="lite-highlight lite-highlight--purple">'
CLOSE_TAG = '</span>'


@register.filter
@stringfilter
@mark_safe
def variable_highlight(value):
    """
    Template tag to highlight variables ({{}} and {%%}) in strings
    """
    # Clean initial value
    value = bleach.clean(value)

    # Wrap {{}} in open and close tag
    rx = '{{ (.+?) }}'
    res = re.sub(rx, (lambda m: f'{OPEN_TAG}{m.group(0)}{CLOSE_TAG}'), value)

    # Wrap {%%} in open and close tag
    rx = '{% (.+?) %}'
    res = re.sub(rx, (lambda m: f'{ALT_OPEN_TAG}{m.group(0)}{CLOSE_TAG}'), res)

    return res
