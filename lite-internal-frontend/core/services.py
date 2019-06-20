from conf.client import get
from conf.constants import DENIAL_REASONS_URL, COUNTRIES_URL, QUEUES_URL
from libraries.forms.components import Option, ArrayQuestion, InputType


def get_denial_reasons(request):
    data = get(request, DENIAL_REASONS_URL).json()
    converted = {}

    for denial_reason in data.get('denial_reasons'):
        item_id = denial_reason['id']

        if not converted.get(item_id[0]):
            converted[item_id[0]] = []

        converted[item_id[0]].append(item_id)

    questions = []
    for key, value in converted.items():
        options = []

        for item in value:
            options.append(Option(item, item))

        questions.append(
            ArrayQuestion('', '', InputType.CHECKBOXES, 'reasons', options, same_row=True)
        )

    return questions


def get_countries(request, convert_to_options=False):
    data = get(request, COUNTRIES_URL)

    if convert_to_options:
        converted_units = []

        for country in data.json().get('countries'):
            converted_units.append(
                Option(country.get('name'), country.get('name'))
            )

        return converted_units

    return data.json(), data.status_code


# Queues


def get_queue(request, pk):
    data = get(request, QUEUES_URL + pk)
    return data.json(), data.status_code


def get_queues(request, convert_to_options=False):
    data = get(request, QUEUES_URL)

    if convert_to_options:
        converted = []

        for queue in data.json().get('queues'):
            converted.append(
                Option(queue.get('id'), queue.get('name'), description=queue.get('team').get('name'))
            )

        return converted

    return data.json(), data.status_code
