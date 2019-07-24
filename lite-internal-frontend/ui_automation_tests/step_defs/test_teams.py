import logging
from pytest_bdd import when, then, parsers, scenarios
from conf.settings import env
import helpers.helpers as utils
from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.teams_pages import TeamsPages

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

sso_email = env('TEST_SSO_EMAIL')
sso_name = env('TEST_SSO_NAME')

scenarios('../features/teams.feature', strict_gherkin=False)


@when('I go to teams')
def go_to_teams(driver):
    header = HeaderPage(driver)

    header.click_lite_menu()
    header.click_teams()


@when('I click on my team')
def click_on_my_team(driver, context):
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
def click_edit_for_my_user(driver):
    driver.find_element_by_xpath("//td[text()='" + sso_email + "']/following-sibling::td[last()]/a").click()


@when(parsers.parse('I add a team called "{team_name}"'))
def add_a_team(driver, team_name, context):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    utils.get_unformatted_date_time()
    teams_pages.click_add_a_team_button()
    if team_name == " ":
        context.team_name = team_name
    else:
        context.team_name = team_name + str(utils.get_unformatted_date_time())
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@when('I add an existing team name')
def add_existing_team(driver, context):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    teams_pages.click_add_a_team_button()
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@when('I edit my team')
def edit_existing_team(driver, context):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    elements = driver.find_elements_by_css_selector(".govuk-table__cell a")
    no = utils.get_element_index_by_text(elements, context.team_name)
    elements[no+1].click()
    context.team_name = context.team_name + "edited"
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@then('I see the team in the team list')
def see_team_in_list(driver, context):
    team_name = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.team_name + "')]]")
    assert team_name.is_displayed()


@then(parsers.parse('I see my teams user list with user "{added_not_added}"'))
def see_team_user_added(driver, added_not_added, context):
    assert driver.find_element_by_tag_name("h1").text == context.team_name , "User is not on teams user list"
    assert Shared(driver).get_text_of_selected_tab() == "USERS" , "Users tab isn't shown"
    if added_not_added == "added":
        table = Shared(driver).get_text_of_table_body()
        assert sso_name in table, "User is not displayed in team list"
        assert sso_email in table, "User is not displayed in team list"
        assert "Active" in table, "User is not displayed in team list"
    elif added_not_added == "not added":
        assert Shared(driver).get_text_of_caption() == "You don't have any users at the moment." , "Users are potentially displayed for a just created Team List"
