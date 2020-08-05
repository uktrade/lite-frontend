from bs4 import BeautifulSoup
import dateparser
import json

from django import template
from django.utils.html import mark_safe


register = template.Library()


@register.filter
def parse_date(date_string):
    if date_string:
        return dateparser.parse(date_string)
    return None


@register.filter
def govuk_css_classes(value):
    soup = BeautifulSoup(value, "html.parser")
    mapping = [
        ("h1", "govuk-heading-xl"),
        ("h2", "govuk-heading-l"),
        ("h3", "govuk-heading-m"),
        ("h4", "govuk-heading-s"),
        ("u", "govuk-heading-s"),
        ("b", "govuk-heading-s"),
        ("h5", "govuk-heading-s"),
        ("h6", "govuk-heading-s"),
        ("ul", "list list-bullet"),
        ("ol", "list list-number"),
        ("p", "govuk-body"),
        ("a", "govuk-link"),
        ("blockquote", "quote"),
        ("strong", "bold-small"),
    ]
    for tag_name, class_name in mapping:
        for element in soup.findAll(tag_name):
            element.attrs["class"] = class_name
    return mark_safe(str(soup))


@register.filter
def pprint_dict(value):
    return json.dumps(value, indent=4)
