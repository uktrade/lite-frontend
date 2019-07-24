import helpers.helpers as utils
from pages.shared import Shared
from pytest_bdd import given, when, then, scenarios
from pages.assign_flags_to_case import CaseFlagsPages
from pages.flags_pages import FlagsPages
from pages.application_page import ApplicationPage
from pages.header_page import HeaderPage

scenarios('../features/assign_case_flags_to_case.feature', strict_gherkin=False)


@given('Case flags have been created')
def case_flags_have_been_created(driver):
    flags = [{'name': 'flag 1', 'level': 'Case'}, {'name': 'flag2', 'level': 'Case'}]

    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_flags()
    flags_page = FlagsPages(driver)

    shared = Shared(driver)

    for flag in flags:
        flags_page.click_add_a_flag_button()
        extra_string = str(utils.get_unformatted_date_time())
        extra_string = extra_string[(len(extra_string)) - 7:]
        flag['name'] = flag['name'] + extra_string
        flags_page.enter_flag_name(flag['name'])
        flags_page.select_flag_level(flag['level'])
        shared.click_submit()


@when("I click edit flags link")
def click_edit_flags_link(driver):
    application_page = ApplicationPage(driver)
    application_page.click_edit_case_flags()


@when('I count the number of assigned flags')
def count_active_flags(driver, context):
    number_of_assigned_flags = FlagsPages(driver).get_size_of_number_of_assigned_flags()
    context.number_of_assigned_flags = number_of_assigned_flags


@when('I assign flags to the case')
def assign_flags_to_case(driver, context):
    case_flags_pages = CaseFlagsPages(driver)
    case_flags_pages.assign_flags(context)
    shared = Shared(driver)
    shared.click_submit()


@when("I unassign flags from the case")
def unassign_flags_from_case(driver, context):
    case_flags_pages = CaseFlagsPages(driver)
    case_flags_pages.assign_flags(context)
    shared = Shared(driver)
    shared.click_submit()


@then("Number of assigned flags is original value")
def assert_number_of_flags(driver, context):
    number_of_assigned_flags = FlagsPages(driver).get_size_of_number_of_assigned_flags()
    assert number_of_assigned_flags == context.number_of_assigned_flags, "number of assigned flags has changed"


@then("Number of assigned flags has increased")
def assert_number_of_flags_has_increased(driver, context):
    number_of_assigned_flags = FlagsPages(driver).get_size_of_number_of_assigned_flags()
    assert number_of_assigned_flags == context.number_of_assigned_flags + 1, "number of assigned flags has not increased"
