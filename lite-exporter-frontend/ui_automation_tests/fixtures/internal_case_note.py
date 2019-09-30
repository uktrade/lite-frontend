from pytest import fixture

from helpers.utils import get_lite_client


@fixture(scope='module')
def internal_case_note(context, api_url):
    lite_client = get_lite_client(context, api_url)
    lite_client.add_case_note(context, context.case_id)


@fixture(scope='module')
def internal_case_note_end_user_advisory(context, api_url):
    lite_client = get_lite_client(context, api_url)
    lite_client.add_case_note(context, context.end_user_advisory_case_id)
