from pytest import fixture


@fixture(scope="session")
def add_an_ecju_query_picklist(api_test_client):
    return api_test_client.picklists.add_ecju_query_picklist()


@fixture(scope="session")
def add_a_proviso_picklist(api_test_client):
    return api_test_client.picklists.add_proviso_picklist()


@fixture(scope="session")
def add_a_standard_advice_picklist(api_test_client):
    return api_test_client.picklists.add_standard_advice_picklist()


@fixture(scope="session")
def add_a_report_summary_picklist(api_test_client):
    return api_test_client.picklists.add_report_summary_picklist()


@fixture(scope="session")
def add_a_letter_paragraph_picklist(api_test_client):
    api_test_client.picklists.add_letter_paragraph_picklist()
