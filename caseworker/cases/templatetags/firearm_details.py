from django import template

register = template.Library()


@register.filter(name="has_added_serial_numbers")
def has_added_serial_numbers(firearm_details):
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
