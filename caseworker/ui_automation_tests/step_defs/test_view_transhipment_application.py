from pytest_bdd import scenarios, given

scenarios("../features/view_transhipment_application.feature", strict_gherkin=False)


@given("a standard transhipment application is created")  # noqa
def a_standard_transhipment_application_is_created(driver, apply_for_standard_transhipment_application):
    pass
