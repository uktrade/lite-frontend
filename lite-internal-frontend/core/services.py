from conf.client import get
from conf.constants import DENIAL_REASONS_URL
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
