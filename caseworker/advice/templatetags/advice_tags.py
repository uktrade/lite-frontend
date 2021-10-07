from django import template


register = template.Library()


@register.filter()
def get_clc(goods):
    clcs = {clc for good in goods for clc in good.get("good", {}).get("control_list_entries", [])}
    return sorted(clcs - {None})


@register.filter()
def get_case_value(goods):
    return sum([float(good.get("value") or "0") for good in goods])


@register.filter()
def get_security_grading(goods):
    gradings = {good.get("good", {}).get("pv_grading_details") for good in goods}
    return sorted(gradings - {None})
