from faker import Faker
from pytest_bdd import scenarios, when, then, given

import shared.tools.helpers as utils
from pages.users_page import UsersPage

scenarios("../features/users.feature", strict_gherkin=False)


@when("I add a new user")
def add_user(driver, context):
    user_page = UsersPage(driver)
    user_page.click_add_a_user_btn()
    fake = Faker()
    context.added_email = fake.email()
    user_page.enter_email(context.added_email)
    user_page.select_option_from_team_drop_down_by_visible_text("Admin")
    user_page.select_option_from_role_drop_down_by_visible_text("Default")
    user_page.click_save_and_continue()


@then("I see new user")
def see_new_user(driver, context):
    assert utils.paginated_item_exists(context.added_email, driver), "Item couldn't be found"


@when("I deactivate new user")
def deactivate_user(driver, context):
    user_page = UsersPage(driver)
    user_page.go_to_users_page(context)
    user_page.deactivate_user()


@then("I dont see new user")
def dont_see_user(driver, context):
    driver.set_timeout_to(0)
    assert utils.paginated_item_exists(context.added_email, driver, exists=False), "Item could be found"
    driver.set_timeout_to(10)


@when("I reactivate new user")
def reactivate_user(driver, context):
    user_page = UsersPage(driver)
    user_page.go_to_users_page(context)
    user_page.reactivate_user()


@when("I edit new user")
def edit_user(driver, context):
    user_page = UsersPage(driver)
    user_page.go_to_users_page(context)
    user_page.click_edit_button_on_users_page()
    context.added_email = context.added_email + "edited"
    user_page.enter_email(context.added_email)

    user_page.select_option_from_team_drop_down_by_value()
    user_page.select_option_from_role_drop_down_by_visible_text("Default")

    # When I Save
    user_page.click_save_and_continue()


@given("I go to users")  # noqa
def go_to_users(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/users/")
