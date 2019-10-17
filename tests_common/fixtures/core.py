from pytest import fixture

from shared.seed_data.manage_s3_documents import upload_test_document_to_aws


@fixture(scope="session")
def context(request):
    class Context(object):
        pass

    return Context()


@fixture(scope="session")
def invalid_username(request):
    return "invalid@mail.com"


@fixture(scope='session')
def exporter_info(request, environment):
    exporter_sso_email = environment('TEST_EXPORTER_SSO_EMAIL')
    exporter_sso_password = environment('TEST_EXPORTER_SSO_PASSWORD')
    first_name = 'Test'
    last_name = 'Lite'

    return {
        'email': exporter_sso_email,
        'password': exporter_sso_password,
        'first_name': first_name,
        'last_name': last_name
    }


@fixture(scope='session')
def internal_info(request, environment):
    gov_user_email = environment('TEST_SSO_EMAIL')
    name = environment('TEST_SSO_NAME')
    gov_user_first_name, gov_user_last_name = name.split(' ')
    gov_user_password = environment('TEST_SSO_PASSWORD')

    return {
        'email': gov_user_email,
        'name': name,
        'first_name': gov_user_first_name,
        'last_name': gov_user_last_name,
        'password': gov_user_password
    }


@fixture(scope='session')
def seed_data_config(request, exporter_info, internal_info):
    api_url = request.config.getoption('--lite_api_url')
    return {
        'api_url': api_url,
        'exporter': exporter_info,
        'gov': internal_info
    }
