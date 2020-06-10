from faker import Faker
from pytest_bdd import scenarios, when, then, given, parsers
from selenium.common.exceptions import NoSuchElementException

from pages.case_list_page import CaseListPage
from pages.users_page import UsersPage

from ui_automation_tests.shared import functions

scenarios("../features/users.feature", strict_gherkin=False)


@when("I add a new user")
def add_user(driver, context):
    user_page = UsersPage(driver)
    user_page.click_add_a_user_button()
    fake = Faker()
    context.added_email = fake.free_email()
    user_page.enter_email(context.added_email)
    user_page.select_option_from_team_drop_down_by_visible_text("Admin")
    user_page.select_option_from_role_drop_down_by_visible_text("Default")
    user_page.select_option_from_default_queue_drop_down_by_visible_text("All cases")
    functions.click_submit(driver)


@then("I see new user")
def see_new_user(driver, context):
    user_page = UsersPage(driver)
    user_page.filter_by_email(context.added_email)
    assert user_page.is_user_email_displayed(context.added_email), "Item couldn't be found"


@when("I deactivate new user")
def deactivate_user(driver, context):
    user_page = UsersPage(driver)
    user_page.go_to_user_page(context)
    user_page.click_deactivate_user()


@then("I dont see new user")
def dont_see_user(driver, context):
    users_page = UsersPage(driver)
    driver.set_timeout_to(0)
    users_page.filter_by_email(context.added_email)
    try:
        users_page.is_user_email_displayed(context.added_email)
    except NoSuchElementException:
        pass
    driver.set_timeout_to_10_seconds()


@when("I reactivate new user")
def reactivate_user(driver, context):
    user_page = UsersPage(driver)
    user_page.go_to_user_page(context)
    user_page.click_reactivate_user()


@when("I edit new user")
def edit_user(driver, context):
    user_page = UsersPage(driver)
    user_page.go_to_user_page(context)
    user_page.click_change_email_link()
    context.added_email = context.added_email + "edited"
    user_page.enter_email(context.added_email)

    user_page.select_option_from_team_drop_down_by_value()
    user_page.select_option_from_role_drop_down_by_visible_text("Default")
    user_page.select_option_from_default_queue_drop_down_by_visible_text("All cases")

    functions.click_submit(driver)


@given("I go to users")  # noqa
def go_to_users(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/users/")


@then("the user's profile is updated")
def users_profile_is_updated(driver, context):
    assert driver.find_element_by_tag_name("h1").text == context.added_email


@when(parsers.parse('I change the user filter to "{status}"'))  # noqa
def filter_status_change(driver, context, status):  # noqa
    CaseListPage(driver).select_filter_user_status_from_dropdown(status)
    CaseListPage(driver).click_apply_filters_button()
