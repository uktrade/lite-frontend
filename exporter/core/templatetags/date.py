import datetime

from django import template


register = template.Library()


@register.filter(name="to_date")
def to_date(val):
    if not val:
        return ""
    return datetime.date.fromisoformat(val)
