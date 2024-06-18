from django import template
from urllib.parse import parse_qs, urlparse

register = template.Library()


@register.filter
def has_param(url, param):
    query = urlparse(url).query
    params = parse_qs(query)
    param_name, expected_value = param.split("=")
    return expected_value in params.get(param_name, [])
