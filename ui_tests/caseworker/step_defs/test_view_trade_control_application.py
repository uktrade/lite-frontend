from pytest_bdd import scenarios, given

scenarios("../features/view_trade_control_application.feature", strict_gherkin=False)


@given("a standard trade control application is created")  # noqa
def a_standard_trade_control_application_is_created(driver, apply_for_standard_trade_control_application):
    pass


@given("an open trade control application is created")  # noqa
def a_standard_trade_control_application_is_created(driver, apply_for_open_trade_control_application):
    pass
