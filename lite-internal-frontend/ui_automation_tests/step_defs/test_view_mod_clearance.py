from pytest_bdd import scenarios, when, then, given

from pages.application_page import ApplicationPage

scenarios("../features/view_mod_clearance.feature", strict_gherkin=False)


@given("an Exhibition Clearance is created")  # noqa
def an_exhibition_clearance_is_created(driver, apply_for_exhibition_clearance):
    pass


@given("a F680 Clearance is created")  # noqa
def an_f680_clearance_is_created(driver, apply_for_f680_clearance):
    pass


@given("a Gifting Clearance is created")  # noqa
def an_gifting_clearance_is_created(driver, apply_for_gifting_clearance):
    pass
