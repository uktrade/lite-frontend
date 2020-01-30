from pytest_bdd import scenarios, given

scenarios("../features/edit_mod_application.feature", strict_gherkin=False)


@given("I create a exhibition clearance application via api")  # noqa
def exhibition_clearance_exists(apply_for_exhibition_clearance):  # noqa
    pass
