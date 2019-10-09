from pytest_bdd import when, then, parsers, scenarios, given
import shared.tools.helpers as utils
from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.teams_pages import TeamsPages
from pages.users_page import UsersPage

scenarios('../features/teams.feature', strict_gherkin=False)


@when('I go to teams via menu')
def go_to_teams_via_menu(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_teams()


@given('I go to teams')
def go_to_teams(driver, sign_in_to_internal_sso, internal_url):
    driver.get(internal_url.rstrip('/') + '/teams/')


@when('I click on my team')
def click_on_my_team(driver, context):
    Shared(driver).scroll_to_bottom_row()
    driver.find_element_by_link_text(context.team_name).click()


@when('I select my newly created team')
def select_team(driver, context):
    TeamsPages(driver).select_team_from_dropdown(context.team_name)
    Shared(driver).click_submit()


@when('I select Admin team')
def select_team(driver):
    TeamsPages(driver).select_team_from_dropdown("Admin")
    Shared(driver).click_submit()


@when('I click edit for my user')
def click_edit_for_my_user(driver, sso_login_info):
    no = utils.get_element_index_by_text(Shared(driver).get_rows_in_lite_table(), sso_login_info['email'])
    Shared(driver).scroll_to_bottom_row()
    UsersPage(driver).click_edit_button_by_index(no)


@when(parsers.parse('I add a team called BlueOcean'))
def add_a_team_blue_ocean(driver, add_a_team, context):
    pass


@when(parsers.parse('I add a team called "{team_name}"'))
def add_a_team(driver, team_name, context):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    utils.get_unformatted_date_time()
    teams_pages.click_add_a_team_button()
    teams_pages.enter_team_name(team_name)
    shared.click_submit()


@when('I edit my team')
def edit_existing_team(driver, context):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    elements = shared.get_links_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.team_name)
    elements[no+1].click()
    context.team_name = context.team_name + "edited"
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@then('I see the team in the team list')
def see_team_in_list(driver, context):
    assert context.team_name in Shared(driver).get_text_of_lite_table_body()


@then(parsers.parse('I see my teams user list with user "{added_not_added}"'))
def see_team_user_added(driver, added_not_added, context, sso_login_info, sso_users_name):
    assert Shared(driver).get_text_of_h1() == context.team_name , "User is not on teams user list"
    assert Shared(driver).get_text_of_selected_tab() == "USERS" , "Users tab isn't shown"
    if added_not_added == "added":
        table = Shared(driver).get_text_of_lite_table_body()
        assert sso_users_name in table, "User is not displayed in team list"
        assert sso_login_info['email'] in table, "User is not displayed in team list"
        assert "Active" in table, "User is not displayed in team list"
    elif added_not_added == "not added":
        assert Shared(driver).get_text_of_caption() == "You don't have any users at the moment." , "Users are potentially displayed for a just created Team List"
