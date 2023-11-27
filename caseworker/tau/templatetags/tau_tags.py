from datetime import datetime
from django import template


register = template.Library()


@register.filter()
def is_ultimate_end_user(destinations):
    """If the case does not have an ultimate_end_user, then the product might be exported onwards to another country"""
    return any(d.get("type") == "ultimate_end_user" for d in destinations)


@register.filter()
def get_destinations(case):
    """Get unique destinations for the case in a nice comma-separated string"""
    unique_destinations = {(dest.get("country") or {}).get("name") or "" for dest in case.destinations}
    return sorted(list(unique_destinations - {""}))


@register.filter
def format_date(val):
    if not val:
        return ""
    date_obj = datetime.strptime(val, "%Y-%m-%d")
    return date_obj.strftime("%d %B %Y")


@register.filter
def parse_tau_assessor(assessor_data):
    """
    Expected format is a list of exactly three items: firstname, lastname, email. # /PS-IGNORE
    """
    if not (type(assessor_data) == list and len(assessor_data) == 3):
        return ""
    tau_assessor_firstname = ""  # /PS-IGNORE
    tau_assessor_lastname = ""  # /PS-IGNORE
    if assessor_data[0] is not None:
        tau_assessor_firstname = assessor_data[0] + " "  # /PS-IGNORE
    if assessor_data[1] is not None:
        tau_assessor_lastname = assessor_data[1]  # /PS-IGNORE
    return tau_assessor_firstname + tau_assessor_lastname  # /PS-IGNORE
