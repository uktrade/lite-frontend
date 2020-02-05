from pytest_bdd import when, then, scenarios

from pages.shared import Shared

scenarios("../features/ecju_queries.feature", strict_gherkin=False)


@when("I go to the recently created application with ecju query")
def click_on_an_application(driver, exporter_url, context, apply_for_standard_application, add_an_ecju_query):
    driver.get(exporter_url.rstrip("/") + "/applications/" + context.app_id)


@when("I click on an CLC query previously created")
def click_on_clc_query(driver, exporter_url, context, add_goods_clc_query):
    driver.get(exporter_url.rstrip("/") + "/goods/" + context.goods_query_good_id)


@then("I see This field may not be blank error message on the page")
def error_message_pop_up(driver):
    shared = Shared(driver)
    assert "This field may not be blank." in shared.get_text_of_error_messages()
