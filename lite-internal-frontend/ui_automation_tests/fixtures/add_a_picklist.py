from pytest import fixture

from shared.tools.utils import get_lite_client


@fixture(scope="session")
def add_an_ecju_query_picklist(context, seed_data_config):
    return get_lite_client(context, seed_data_config).seed_picklist.add_ecju_query_picklist()


@fixture(scope="session")
def add_a_proviso_picklist(context, seed_data_config):
    return get_lite_client(context, seed_data_config).seed_picklist.add_proviso_picklist()


@fixture(scope="session")
def add_a_standard_advice_picklist(context, seed_data_config):
    return get_lite_client(context, seed_data_config).seed_picklist.add_standard_advice_picklist()


@fixture(scope="session")
def add_a_report_summary_picklist(context, seed_data_config):
    return get_lite_client(context, seed_data_config).seed_picklist.add_report_summary_picklist()


@fixture(scope="session")
def add_a_letter_paragraph_picklist(context, seed_data_config):
    get_lite_client(context, seed_data_config).seed_picklist.add_letter_paragraph_picklist()
