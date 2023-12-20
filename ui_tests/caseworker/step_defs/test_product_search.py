import json

from datetime import datetime

from pytest_bdd import scenarios, given, then, when, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests_common import functions
from ui_tests.caseworker.pages.product_search import ProductSearchPage


scenarios("../features/product_search.feature", strict_gherkin=False)


@given(parsers.parse("I add my assessment as TAU case advisor as json:\n{assessment_data}"))
def add_products_assessments(api_test_client, context, assessment_data):
    assessments = json.loads(assessment_data.replace("\n", ""))
    assert len(context.good_on_application_ids) == len(assessments)

    payload = []
    for index, assessment in enumerate(assessments):
        assessment_item = {
            **assessment,
            "id": context.good_on_application_ids[index],
            "is_good_controlled": True,
            "is_ncsc_military_information_security": False,
        }
        payload.append(assessment_item)

    response = api_test_client.api_client.make_request(
        method="PUT",
        url=f"/assessments/make-assessments/{context.application_id}/",
        headers=api_test_client.api_client.gov_headers,
        body=payload,
    )
    assert response.status_code == 200


@when("I go to product search page")
def go_to_product_search_page(driver):
    WebDriverWait(driver, 30).until(
        expected_conditions.presence_of_element_located((By.ID, "link-product-search"))
    ).click()


@when(parsers.parse('I start typing "{search_text}" in search field'))
def enter_search_text(driver, search_text):
    ProductSearchPage(driver).enter_search_text(search_text)


@when(parsers.parse('I enter search string as "{search_text}" and submit'))
def enter_search_text(driver, search_text):
    ProductSearchPage(driver).enter_search_text(search_text)
    functions.click_submit(driver)


@then(parsers.parse('I should see "{num_suggestions}" suggestions related to "{field}" with values "{field_values}"'))
def enter_search_text(driver, num_suggestions, field, field_values):
    suggestions = ProductSearchPage(driver).get_current_suggestions()

    suggestions_for_field = [s for s in suggestions if s["key"] == field]
    assert len(suggestions_for_field) == int(num_suggestions)
    actual_values = sorted([s["value"] for s in suggestions if s["key"] == field])
    expected = sorted(field_values.split(","))
    assert actual_values == expected


@when(parsers.parse('I select suggestion for "{field}" with value "{value}" and submit'))
def select_suggestion_with_value(driver, field, value):
    ProductSearchPage(driver).select_suggestion(field, value)
    functions.click_submit(driver)


@then(parsers.parse("I see below search results as json:\n{results_data}"))
def verify_search_results(driver, results_data):
    results = json.loads(results_data.replace("\n", ""))

    result_elements = []
    results_section = driver.find_element(by=By.CLASS_NAME, value="search-results")
    # check if there non-zero search results
    # otherwise find_elements() waits for timeout
    if results_section.text != "":
        result_elements = driver.find_elements(by=By.CLASS_NAME, value="search-result")

    assert len(result_elements) == results["num_results"]

    for index, element in enumerate(result_elements):
        actual = ProductSearchPage(driver).get_result_row_data(element)
        expected = results["hits"][index]
        expected["Assessment date"] = datetime.today().strftime("%d %B %Y")

        for key in expected.keys():
            assert expected[key] == actual[key]
