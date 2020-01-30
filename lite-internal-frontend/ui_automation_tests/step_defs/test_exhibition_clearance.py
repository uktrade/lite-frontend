from pytest_bdd import scenarios, when, then, given

from pages.application_page import ApplicationPage

scenarios("../features/exhibition_clearance.feature", strict_gherkin=False)


@given("an Exhibition Clearance is created")  # noqa
def an_exhibition_clearance_is_created(driver, apply_for_exhibition_clearance):
    pass


@when("I click on the Exhibition Clearance case")  # noqa
def i_click_on_the_exhibition_clearance_case(driver, context):
    driver.find_element_by_link_text(context.reference_code).click()


@then("I see the Exhibition Clearance case page")  # noqa
def i_see_the_exhibition_clearance_case_page(driver, context):
    assert driver.find_element_by_id(ApplicationPage.HEADING_ID).text == context.reference_code
