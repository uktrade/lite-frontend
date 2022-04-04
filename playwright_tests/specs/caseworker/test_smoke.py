import pytest

from playwright_tests.api.create_application import create_application
from playwright_tests.selectors.cases import case_selectors

FCDO_REASON = "FCDO Approval Reason"
COUNTER_SIGN_REASON = "Countersign Approval Reason"


@pytest.fixture(scope="session", autouse=True)
def application_data():
    return create_application()


def test_smoke(page, application_data):
    page.goto("/")
    page.goto(f"/queues/{application_data['default_queue']}/cases/{application_data['application_id']}/")

    header = page.locator(case_selectors["header"])
    assert application_data["submitted_application"]["reference_code"] in header.text_content()
