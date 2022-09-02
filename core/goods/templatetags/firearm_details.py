from django import template

from core.goods.helpers import is_product_category_made_before_1938


register = template.Library()


@register.filter(name="has_added_serial_numbers")
def has_added_serial_numbers(firearm_details):
    if not firearm_details:
        return False
    try:
        serial_numbers_available = firearm_details["serial_numbers_available"]
    except KeyError:
        return False

    if serial_numbers_available == "NOT_AVAILABLE":
        return False

    try:
        serial_numbers = firearm_details["serial_numbers"]
    except KeyError:
        return False

    added_serial_numbers = [sn for sn in serial_numbers if sn]

    return len(added_serial_numbers) > 0


@register.filter(name="is_made_before_1938_category")
def is_made_before_1938_category(firearm_details):
    return is_product_category_made_before_1938(firearm_details)
