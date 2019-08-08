from pytest import fixture
import helpers.helpers as utils
from pages.shared import Shared
from pages.teams_pages import TeamsPages


@fixture(scope="session")
def add_a_team(driver, context):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    teams_pages.click_add_a_team_button()
    context.team_name = "BlueOcean" + str(utils.get_unformatted_date_time())
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()
