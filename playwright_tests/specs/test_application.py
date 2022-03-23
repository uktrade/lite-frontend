import pytest

from playwright_tests.api.create_application import create_application
from playwright_tests.selectors.cases import case_selectors

FCDO_REASON = "FCDO Approval Reason"
COUNTER_SIGN_REASON = "Countersign Approval Reason"


@pytest.fixture(scope="session", autouse=True)
def application_data():
    return create_application()


def test_approve_a_case_in_FCDO_queue(page, application_data):
    page.goto("/")
    page.goto(f"/queues/{application_data['default_queue']}/cases/{application_data['application_id']}/")

    header = page.locator(case_selectors["header"])
    assert application_data["submitted_application"]["reference_code"] in header.text_content()

    page.goto(f"/queues/{application_data['default_queue']}/cases/{application_data['application_id']}/advice")
    page.locator(case_selectors["make_recommendation"]).click()
    page.locator(case_selectors["approve_all"]).click()
    page.locator(case_selectors["continue"]).click()
    page.locator(case_selectors["belgium_checkbox"]).click()
    page.locator(case_selectors["ukraine_checkbox"]).click()

    page.locator(case_selectors["fcdo_approval_reason"]).fill(FCDO_REASON)
    page.locator(case_selectors["continue"]).click()

    recommendation_review = page.locator(case_selectors["recommendation_review"]).inner_text()

    for expected_text in ["Approved by first-name last-name", "Belgium", "Ukraine", FCDO_REASON]:
        assert expected_text in recommendation_review

    page.locator(case_selectors["continue"]).click()
    page.goto(
        f"/queues/{application_data['default_queue']}/?case_reference={application_data['submitted_application']['reference_code']}"
    )
    case_form = page.locator(case_selectors["recommendation_review"]).text_content()
    assert "There are no new cases" in case_form


def test_approve_a_case_in_FCO_countersign_queue(page, application_data):
    COUNTER_SIGN_QUEUE = "5e772575-9ae4-4a16-b55b-7e1476d810c4"

    page.goto("/")
    page.goto(f"/queues/{COUNTER_SIGN_QUEUE}/cases/{application_data['application_id']}/details/")

    assigned_queues = page.locator(case_selectors["assigned_queues"]).inner_text()

    assert "FCO Cases to Review" not in assigned_queues
    assert "FCDO Counter-signing" in assigned_queues

    page.goto(f"/queues/{COUNTER_SIGN_QUEUE}/cases/{application_data['application_id']}/advice/countersign/")
    counter_sign_details = page.locator(case_selectors["counter_sign_details"]).inner_text()
    for expected_text in ["Belgium", "Ukraine", FCDO_REASON]:
        assert expected_text in counter_sign_details

    page.goto(f"/queues/{COUNTER_SIGN_QUEUE}/cases/{application_data['application_id']}/advice/countersign/")
    page.locator(case_selectors["make_recommendation"]).click()
    page.locator(case_selectors["counter_sign_approval_reason"]).fill(COUNTER_SIGN_REASON)
    page.locator(case_selectors["continue"]).click()

    counter_sign_reason = page.locator(case_selectors["counter_sign_reason"]).inner_text()
    assert COUNTER_SIGN_REASON in counter_sign_reason

    fcdo_reason = page.locator(case_selectors["fcdo_reason"]).inner_text()
    assert FCDO_REASON in fcdo_reason

    page.locator(case_selectors["continue"]).click()
    page.goto(f"/queues/{COUNTER_SIGN_QUEUE}/cases/{application_data['application_id']}/details/")

    assigned_queues = page.locator(case_selectors["assigned_queues"]).inner_text()
    assert "FCO Cases to Review" not in assigned_queues
    assert "FCDO Counter-signing" not in assigned_queues
    assert "MOD Cases to Review" in assigned_queues
