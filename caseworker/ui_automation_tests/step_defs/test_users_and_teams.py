from faker import Faker
from pytest_bdd import scenarios, when, then, given, parsers
from selenium.common.exceptions import NoSuchElementException
import shared.tools.helpers as utils

from pages.case_list_page import CaseListPage
from pages.shared import Shared
from pages.teams_pages import TeamsPages
from pages.users_page import UsersPage

from ui_automation_tests.shared import functions

scenarios("../features/users_and_teams.feature", strict_gherkin=False)


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
    driver.implicitly_wait(0)
    users_page.filter_by_email(context.added_email)
    try:
        users_page.is_user_email_displayed(context.added_email)
    except NoSuchElementException:
        pass
    driver.implicitly_wait(10)


@when("I reactivate new user")
def reactivate_user(driver, context):
    user_page = UsersPage(driver)
    user_page.go_to_user_page(context)
    user_page.click_reactivate_user()


@when("I go to edit new user")
def edit_user(driver, context):
    user_page = UsersPage(driver)
    user_page.go_to_user_page(context)
    user_page.click_change_email_link()


@when("I edit new users email and save")
def edit_user(driver, context):
    context.added_email = context.added_email + "edited"
    user_page = UsersPage(driver)
    user_page.enter_email(context.added_email)
    Shared(driver).click_submit()


@given("I go to users")  # noqa
def go_to_users(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/users/")


@then("the user's profile is updated")
def users_profile_is_updated(driver, context):
    assert driver.find_element_by_tag_name("h1").text == context.added_email


@when(parsers.parse('I change the user filter to "{status}"'))  # noqa
def filter_status_change(driver, context, status):  # noqa
    CaseListPage(driver).select_filter_user_status_from_dropdown(status)
    functions.click_apply_filters(driver)


@when("I go to teams")
def go_to_teams(driver, sso_sign_in, internal_url):
    driver.get(internal_url.rstrip("/") + "/teams/")


@when("I click on the team BlueOcean")
def click_on_my_team(driver, context):
    driver.find_element_by_link_text(context.team_name).click()


@when("I select my newly created team")
def select_team(driver, context):
    TeamsPages(driver).select_team_from_dropdown(context.team_name)
    TeamsPages(driver).select_default_queue_from_dropdown("All cases")


@when(parsers.parse("I add a team called BlueOcean"))
def add_a_team_blue_ocean(driver, context):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    teams_pages.click_add_a_team_button()
    context.team_name = "BlueOcean" + str(utils.get_formatted_date_time_y_m_d_h_s())
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@when("I edit my team")
def edit_existing_team(driver, context):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    elements = shared.get_links_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.team_name)
    elements[no + 1].click()
    context.team_name = context.team_name + "edited"
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@then("I see the team in the team list")
def see_team_in_list(driver, context):
    assert context.team_name in Shared(driver).get_text_of_lite_table_body()


@then(parsers.parse('I see my teams user list with user "{added_not_added}"'))
def see_team_user_added(driver, added_not_added, context, internal_info):
    if added_not_added == "added":
        table = Shared(driver).get_text_of_lite_table_body()
        assert context.added_email in table, "User is not displayed in team list"
        assert "Active" in table, "User is not displayed in team list"
    elif added_not_added == "not added":
        assert functions.element_with_css_selector_exists(
            driver, Shared(driver).LITE_NOTICE_SELECTOR
        ), "Users are potentially displayed for a just created Team List"
