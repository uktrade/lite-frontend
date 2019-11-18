from pytest_bdd import when, then, given, parsers, scenarios

from shared import functions
from pages.application_page import ApplicationPage
from pages.exporter_hub_page import ExporterHubPage
from pages.respond_to_ecju_query_page import RespondToEcjuQueryPage
from pages.shared import Shared

scenarios("../features/ecju_queries.feature", strict_gherkin=False)


@given("An application exists and a ecju query has been added via internal gov site")
def application_exists_ecju_query_added(apply_for_standard_application, add_an_ecju_query):
    pass


@when("I go to the recently created application")
def click_on_an_application(driver, exporter_url, context, apply_for_standard_application, add_an_ecju_query):
    driver.get(exporter_url.rstrip("/") + "/applications/" + context.app_id)


@when("I select to view ecju queries")
def click_ecju_query_tab(driver):
    application_page = ApplicationPage(driver)
    application_page.click_ecju_query_tab()


@when("I click to view goods page")
def click_on_goods_page(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_my_goods()


@when("I click on an CLC query previously created")
def click_on_clc_query(driver, exporter_url, context, add_clc_query):
    driver.get(exporter_url.rstrip("/") + "/goods/" + context.clc_good_id)


@when("I click to respond to the ecju query")
def click_ecju_query_tab(driver):
    application_page = ApplicationPage(driver)
    application_page.respond_to_ecju_query(0)


@when(parsers.parse('I enter "{response}" for ecju query and click submit'))
def respond_to_query(driver, response):
    response_page = RespondToEcjuQueryPage(driver)
    response_page.enter_form_response(response)
    functions.click_submit(driver)


@when(parsers.parse('I select "{value}" for submitting response and click submit'))
def submit_response_confirmation(driver, value):
    driver.find_element_by_xpath('//input[@value="' + value + '"]').click()
    driver.find_element_by_xpath('//button[@type="submit"]').click()


@then("I see my ecju query is closed")
def determine_that_there_is_a_closed_query(driver):
    application_page = ApplicationPage(driver)
    closed_queries = application_page.get_count_of_closed_ecju_queries()
    assert closed_queries > 0


@then("I see This field may not be blank error message on the page")
def error_message_pop_up(driver):
    shared = Shared(driver)
    assert "This field may not be blank." in shared.get_text_of_error_messages()
