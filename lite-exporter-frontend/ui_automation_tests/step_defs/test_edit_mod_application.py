from pytest_bdd import scenarios, given, when

scenarios("../features/edit_mod_application.feature", strict_gherkin=False)


@given("I create a exhibition clearance application via api")  # noqa
def exhibition_clearance_exists(apply_for_exhibition_clearance):  # noqa
    pass


@given("I create a F680 clearance application via api")  # noqa
def f680_clearance_exists(apply_for_f680_clearance):  # noqa
    pass


@given("I create a gifting clearance application via api")  # noqa
def gifting_clearance_exists(apply_for_gifting_clearance):  # noqa
    pass
