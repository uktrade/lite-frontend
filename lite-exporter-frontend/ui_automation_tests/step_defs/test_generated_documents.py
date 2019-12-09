from pytest_bdd import when, scenarios, then

from pages.application_page import ApplicationPage

scenarios("../features/generated_documents.feature", strict_gherkin=False)


@when("I go to the recently created application with a Generated Document attached")
def click_on_an_application(driver, exporter_url, context, apply_for_standard_application, add_a_generated_document):
    driver.get(exporter_url.rstrip("/") + "/applications/" + context.app_id)


@when("I click the Generated Documents tab")  # noqa
def click_generated_documents_tab(driver):
    application_page = ApplicationPage(driver)
    application_page.click_generated_documents_tab()


@then("I can see the Generated Document")
def i_can_see_the_generated_document(driver):
    application_page = ApplicationPage(driver)
    assert application_page.generated_documents_count() == 1
