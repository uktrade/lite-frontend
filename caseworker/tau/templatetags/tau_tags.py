from django import template


register = template.Library()


@register.filter()
def is_ultimate_end_user(destinations):
    """If the case does not have an ultimate_end_user, then the product might be exported onwards to another country"""
    return {d for d in destinations if d.get("type") == "ultimate_end_user"} != {}
