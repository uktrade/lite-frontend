from bs4 import BeautifulSoup
from pytest_bdd import given, when, then, scenarios, parsers
from selenium.webdriver.common.by import By

from caseworker.core.constants import SystemTeamsID
from ui_tests.caseworker.pages.application_page import ApplicationPage
from ui_tests.caseworker.pages.case_page import CasePage
from ui_tests.caseworker.pages.routing_rules_pages import RoutingRulesPage
from ui_tests.caseworker.pages.teams_pages import TeamsPages
from tests_common import functions

scenarios("../features/routing_rules.feature", strict_gherkin=False)


@when("I go to routing rules list")
def go_to_routing_rules(driver, sso_sign_in, internal_url):
    driver.get(internal_url.rstrip("/") + "/routing-rules/")


@then("I see the routing rule in the rule list")
def see_flag_in_list(driver, context):
    assert driver.find_element_by_id(context.queue_id).is_displayed()


@when(
    parsers.parse(
        'I add a routing rule of tier "{tier}", a status of "{case_status}", my queue, and all additional rules for my team'
    )
)
def create_routing_rule(driver, context, tier, case_status):
    routing_rules_page = RoutingRulesPage(driver)
    routing_rules_page.create_new_routing_rule()
    routing_rules_page.select_team(SystemTeamsID.ADMIN.value)
    functions.click_submit(driver)
    routing_rules_page.initial_details_form(
        tier=tier, case_status=case_status, queue=context.queue_name, additional_rules=True
    )
    functions.click_submit(driver)

    routing_rules_page.select_case_type_by_text("Standard-Individual-Export-Licence")
    functions.click_submit(driver)

    routing_rules_page.select_flag(context.flag_name)
    functions.click_submit(driver)

    routing_rules_page.enter_country("China")
    functions.click_submit(driver)

    routing_rules_page.select_first_user()
    functions.click_submit(driver)


@when(
    parsers.parse(
        'I add a routing rule of tier "{tier}", a status of "{case_status}", my queue, and no additional rules for my team'
    )
)
def create_routing_rule(driver, context, tier, case_status):
    routing_rules_page = RoutingRulesPage(driver)
    routing_rules_page.create_new_routing_rule()
    routing_rules_page.select_team(SystemTeamsID.ADMIN.value)
    functions.click_submit(driver)
    routing_rules_page.initial_details_form(
        tier=tier, case_status=case_status, queue=context.queue_name, additional_rules=False
    )
    functions.click_submit(driver)


@when(parsers.parse('I edit my routing rule with tier "{tier}", a status of "{case_status}", and no additional rules'))
def edit_flagging_rule(driver, context, tier, case_status):
    routing_rules_page = RoutingRulesPage(driver)
    routing_rules_page.edit_row_by_queue_id(context.queue_id)
    routing_rules_page.initial_details_form(tier=tier, case_status=case_status, additional_rules=False)
    functions.click_submit(driver)


@then(parsers.parse('I see the routing rule in the list as "{status}" and tier "{tier}"'))
def routing_rule_status(driver, context, status, tier):
    routing_rules_page = RoutingRulesPage(driver)
    text = routing_rules_page.find_row_by_queue_id(context.queue_id).text
    assert status in text
    assert tier in text


@when("I deactivate my routing rule")
def deactivate_rule(driver, context):
    routing_rules_page = RoutingRulesPage(driver)
    row = routing_rules_page.find_row_by_queue_id(context.queue_id)
    routing_rules_page.click_on_deactivate_rule(row)
    routing_rules_page.click_confirm_deactivate_activate()
    functions.click_submit(driver)


@when("I click to rerun routing rules, and confirm")
def rerun_routing_rules(driver):
    application_page = ApplicationPage(driver)
    CasePage(driver).click_rerun_routing_rules()
    application_page.click_confirm_rerun_routing_rules()
    functions.click_submit(driver)


@then("I see my queue in assigned queues")
def i_see_my_queue_in_queues_to_the_case_on_page(driver, context):
    assert context.queue_name in ApplicationPage(driver).get_case_queues().text


@when("I filter by my routing rule queue")
def filter_by_routing_rule_queue(driver, context):
    RoutingRulesPage(driver).filter_by_queue_name(context.queue_name)


@when("I add a flag at level Case")  # noqa
def add_a_case_flag(driver, add_case_flag):  # noqa
    pass


@when(parsers.parse('I change my default queue to "{queue}"'))  # noqa
def go_to_team_edit_page(driver, team, queue):  # noqa
    # we should already be on the profile page
    driver.find_element_by_id("link-edit-team").click()
    teams_page = TeamsPages(driver)
    teams_page.select_team_from_dropdown(team)
    teams_page.select_default_queue_from_dropdown(queue)
    functions.click_submit(driver)


@when("I click on the application previously created")
def click_on_case(driver, context):
    driver.find_element(by=By.ID, value=f"case-{context.case_id}").click()


@then('I should see the button "I\'m done"')
def done_button_on_page(driver):
    assert driver.find_element(by=By.ID, value="button-done")


@then("the case should have been removed from my default queue")
def case_removed_from_queue(driver, context):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    assert not soup.find(id=f"case-{context.case_id}")


@given(parsers.parse('I set the case status to "{status}"'))
def set_case_status(driver, status, api_test_client, context):
    api_test_client.cases.manage_case_status(api_test_client.context["case_id"], status=status.lower())
