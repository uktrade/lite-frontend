from pytest_bdd import when, scenarios, then, given

from ui_automation_tests.pages.application_page import ApplicationPage

scenarios("../features/generated_documents.feature", strict_gherkin=False)


@given("A document has been generated for my application")
def click_on_an_application(add_a_generated_document):
    pass


@when("I click the Generated Documents tab")  # noqa
def click_generated_documents_tab(driver):
    application_page = ApplicationPage(driver)
    application_page.click_generated_documents_tab()


@then("I can see the Generated Document")
def i_can_see_the_generated_document(driver):
    application_page = ApplicationPage(driver)
    assert application_page.generated_documents_notification_count() == "1"
    assert application_page.generated_documents_count() == 1
