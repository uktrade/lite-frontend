from playwright_tests.api.create_application import create_application
from playwright_tests.selectors.cases import case_selectors


def test_approve_a_case_in_FCDO_queue(page):
    FCDO_REASON = "FCDO Approval Reason"

    response = create_application()
    page.goto("/")
    page.goto(f"/queues/{response['default_queue']}/cases/{response['application_id']}/")

    header = page.locator(case_selectors["header"])
    assert response["submitted_application"]["reference_code"] in header.text_content()

    page.goto(f"/queues/{response['default_queue']}/cases/{response['application_id']}/advice")
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
        f"/queues/{response['default_queue']}/?case_reference={response['submitted_application']['reference_code']}"
    )
    case_form = page.locator(case_selectors["recommendation_review"]).text_content()
    assert "There are no new cases" in case_form
