from django import template


register = template.Library()


@register.filter()
def get_clc(goods):
    clcs = {clc["rating"] for good in goods for clc in good.get("good", {}).get("control_list_entries", []) if clc}
    return sorted(clcs - {None})


@register.filter()
def get_case_value(goods):
    return sum([float(good.get("value") or "0") for good in goods])


@register.filter()
def get_security_grading(goods):
    gradings = {good.get("good", {}).get("pv_grading_details") for good in goods}
    return sorted(gradings - {None})


@register.filter
def index(iter, i):
    return iter[i]


@register.filter
def advice_given_by(advice):
    return f"{advice['user']['first_name']} {advice['user']['last_name']}"


@register.filter
def countersigned_user_team(advice):
    return f"{advice['countersigned_by']['team']['name']}"
