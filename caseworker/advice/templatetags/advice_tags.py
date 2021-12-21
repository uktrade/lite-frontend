from django import template


register = template.Library()


@register.filter()
def get_clc(goods):
    clcs = {clc["rating"] for good in goods for clc in good.get("good", {}).get("control_list_entries", []) if clc}
    return sorted(clcs - {None})


@register.filter()
def get_case_value(goods):
    return f'{sum([float(good.get("value") or "0") for good in goods]):.2f}'


@register.filter
def is_case_pv_graded(products):
    """Returns True if pv_grading is True for atleast one of the products on the application"""
    gradings = {product.get("good", {}).get("is_pv_graded") for product in products}
    return "yes" in gradings


@register.filter
def index(array, i):
    return array[i]


@register.filter
def get_item(dict, key):
    return dict.get(key, "")


@register.filter
def countersigned_user_team(advice):
    return f"{advice['countersigned_by']['team']['name']}"
