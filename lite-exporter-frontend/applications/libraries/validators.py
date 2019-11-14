from http import HTTPStatus


def validate_external_location_choice(_request, _pk, json):
    if json.get('choice'):
        return json, HTTPStatus.OK

    return {'errors': {'choice': ['Select a choice']}}, HTTPStatus.BAD_REQUEST
