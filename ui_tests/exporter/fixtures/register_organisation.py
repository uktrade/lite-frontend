from pytest import fixture
from random import randint

from tests_common.tools.utils import Timer


@fixture(scope="session")
def register_organisation(context, api_test_client):
    timer = Timer()
    context.org_registered_status = True
    context.first_name = api_test_client.context["first_name"]
    context.last_name = api_test_client.context["last_name"]
    context.org_name = api_test_client.context["org_name"]
    context.org_id = api_test_client.context["org_id"]
    timer.print_time("register_organisation")


@fixture(scope="session")
def register_organisation_for_switching_organisation(context, api_test_client):
    api_test_client.organisations.setup_org_for_switching_organisations()
    context.org_name_for_switching_organisations = api_test_client.context["org_name_for_switching_organisations"]


@fixture(scope="function")
def get_eori_number():
    return "GB" + "".join(["{}".format(randint(0, 9)) for _ in range(12)])


@fixture(scope="function")
def get_registration_number():
    return "".join([str(randint(0, 9)) for _ in range(8)])
