from pytest_bdd import scenarios, given, when, then

from ui_automation_tests.pages.standard_application.goods import StandardApplicationGoodsPage
from ui_automation_tests.shared.fixtures.apply_for_application import apply_for_trade_control_application

scenarios("../features/edit_trade_control_application.feature", strict_gherkin=False)


@given("I create a trade control application via api")  # noqa
def trade_control_application_exists(apply_for_trade_control_application):  # noqa
    pass


@when("I remove a location from the application")
def i_remove_a_location_from_the_application(driver):  # noqa
    StandardApplicationGoodsPage(driver).get_remove_location_link().click()


@then("the location has been removed from the application")
def no_locations_are_left_on_the_application(driver):  # noqa
    assert not StandardApplicationGoodsPage(driver).find_remove_location_link()
