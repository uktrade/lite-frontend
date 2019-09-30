from pytest import fixture

from helpers.utils import get_lite_client


@fixture(scope='function')
def add_clc_query(driver, request, context, exporter_url, api_url):
    lite_client = get_lite_client(context, api_url)
    lite_client.add_clc_good()
    context.clc_good_id = lite_client.context['clc_good_id']
