from pytest import fixture

from helpers.utils import get_lite_client


@fixture(scope='session')
def add_an_ecju_query_picklist(context, api_url):
    return get_lite_client(context, api_url).add_ecju_query_picklist()


@fixture(scope='session')
def add_a_proviso_picklist(context, api_url):
    return get_lite_client(context, api_url).add_proviso_picklist()


@fixture(scope='session')
def add_a_standard_advice_picklist(context, api_url):
    return get_lite_client(context, api_url).add_standard_advice_picklist()


@fixture(scope='session')
def add_a_report_summary_picklist(context, api_url):
    return get_lite_client(context, api_url).add_report_summary_picklist()
