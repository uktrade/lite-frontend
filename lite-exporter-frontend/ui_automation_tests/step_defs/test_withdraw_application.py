from pytest_bdd import scenarios, then, when, parsers

from pages.application_page import ApplicationPage
from shared import selectors
from shared.functions import element_with_id_exists

scenarios("../features/withdraw_application.feature", strict_gherkin=False)


@when("I click the button 'Withdraw Application'")
def i_click_withdraw_application(driver):
    ApplicationPage(driver).click_withdraw_application_button()


@then("I should see a confirmation page")
def i_should_see_a_confirmation_page(driver):
    assert len(driver.find_elements_by_css_selector(selectors.RADIO_BUTTONS)) == 2


@when("I select the yes radiobutton")
def i_select_the_yes_radiobutton(driver):
    driver.find_element_by_id("choice-yes").click()


@then(parsers.parse('the application will have the status "{status}"'))
def the_application_will_have_status(driver, status):
    assert ApplicationPage(driver).get_status() == status


@then("I won't be able to see the withdraw button")
def i_wont_be_able_to_see_the_withdraw_button(driver):
    driver.set_timeout_to(0)
    assert not element_with_id_exists(driver, ApplicationPage.BUTTON_WITHDRAW_APPLICATION_ID)
    driver.set_timeout_to(10)
