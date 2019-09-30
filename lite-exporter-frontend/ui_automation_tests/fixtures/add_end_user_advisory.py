from pytest import fixture

from helpers.utils import get_lite_client


@fixture(scope='module')
def add_end_user_advisory(driver, request, context, exporter_url, api_url):
    lite_client = get_lite_client(context, api_url)
    lite_client.add_eua_query()
    context.end_user_advisory_id = lite_client.context['end_user_advisory_id']
    context.end_user_advisory_case_id = lite_client.context['end_user_advisory_case_id']
