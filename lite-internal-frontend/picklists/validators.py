from http import HTTPStatus

from picklists.helpers import picklist_paragraph_errors
from picklists.services import post_picklist_item, put_picklist_item


def validate_and_post_picklist_item(request, json):
    if json.get("type") == "letter_paragraph":
        errors = picklist_paragraph_errors(request)
        if errors:
            return errors, HTTPStatus.BAD_REQUEST

    return post_picklist_item(request, json)


def validate_and_put_picklist_item(request, pk, json):
    if json.get("type") == "letter_paragraph":
        errors = picklist_paragraph_errors(request)
        if errors:
            return errors, HTTPStatus.BAD_REQUEST

    return put_picklist_item(request, pk, json)
