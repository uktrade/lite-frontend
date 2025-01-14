import json

from datetime import datetime

from pytest_bdd import scenarios, then, when, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests_common import functions
from django.conf import settings
from ui_tests.caseworker.pages.product_search import ProductSearchPage


scenarios("../features/product_search.feature", strict_gherkin=False)


@when("I go to product search page")
def go_to_product_search_page(driver):
    WebDriverWait(driver, 30 * settings.E2E_WAIT_MULTIPLIER).until(
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

    # As other tests can create products in the db there can be more than the
    # expected number of suggestions hence collect all results and check for
    # the presence of expected suggestions in those results
    suggestions_for_field = [s for s in suggestions if s["key"] == field]
    assert len(suggestions_for_field) >= int(num_suggestions)

    actual_values = {s["value"] for s in suggestions if s["key"] == field}
    expected = set(field_values.split(","))
    assert expected.intersection(actual_values) == expected


@when(parsers.parse('I select suggestion for "{field}" with value "{value}" and submit'))
def select_suggestion_with_value(driver, field, value):
    ProductSearchPage(driver).select_suggestion(field, value)
    functions.click_submit(driver)


@then(parsers.parse("I should see below hit in search results as json:\n{results_data}"))
def verify_search_results(driver, results_data):
    results = json.loads(results_data.replace("\n", ""))

    result_elements = []
    results_section = driver.find_element(by=By.CLASS_NAME, value="search-results")
    # check if there non-zero search results
    # otherwise find_elements() waits for timeout
    if results_section.text != "":
        result_elements = driver.find_elements(by=By.CLASS_NAME, value="search-result")

    # As other tests can create products in the db there can be more than the
    # expected number of results hence collect all results and check for
    # the presence of expected hit in those results
    assert len(result_elements) >= results["num_results"]

    actual_results = [ProductSearchPage(driver).get_result_row_data(element) for element in result_elements]

    for expected_hit in results["hits"]:
        expected_hit["Assessment date"] = datetime.today().strftime("%-d %B %Y")

        matching_results = [item for item in actual_results if item["name"] == expected_hit["name"]]
        assert len(matching_results) == 1

        actual_result = matching_results[0]
        for key in expected_hit.keys():
            assert expected_hit[key] == actual_result[key]
