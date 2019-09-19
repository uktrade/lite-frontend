from lite_forms.components import Option, Checkboxes

from conf.client import get
from conf.constants import DENIAL_REASONS_URL, COUNTRIES_URL, STATUSES_URL
from users.services import get_gov_user


def get_denial_reasons(request, convert_to_options=True):
    data = get(request, DENIAL_REASONS_URL)
    status_code = data.status_code
    data = data.json()

    converted = {}

    for denial_reason in data.get('denial_reasons'):
        item_id = denial_reason['id']

        if not converted.get(item_id[0]):
            converted[item_id[0]] = []

        converted[item_id[0]].append(item_id)

    if convert_to_options:
        questions = []
        for _, value in converted.items():
            options = []

            for item in value:
                options.append(Option(item, item))

            questions.append(
                Checkboxes('reasons', options, description='')
            )

        return questions
    else:
        return converted, status_code


def get_countries(request, convert_to_options=False):
    data = get(request, COUNTRIES_URL)

    if convert_to_options:
        converted_units = []

        for country in data.json().get('countries'):
            converted_units.append(
                Option(country.get('id'), country.get('name'))
            )

        return converted_units

    return data.json(), data.status_code


# Statuses

def get_statuses(request):
    data = get(request, STATUSES_URL)
    return data.json(), data.status_code


# Permissions

def get_user_permissions(request, with_team=False):
    user, _ = get_gov_user(request, str(request.user.lite_api_user_id))
    if with_team:
        return user['user']['role']['permissions'], user['user']['team']
