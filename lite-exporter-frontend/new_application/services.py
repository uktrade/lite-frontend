from conf.client import get
from conf.constants import UNITS_URL
from libraries.forms.components import Option


def get_units(request):
    data = get(request, UNITS_URL).json()
    converted_units = []

    for key, value in data.get('units').items():
        converted_units.append(
           Option(key, value)
        )

    return converted_units
