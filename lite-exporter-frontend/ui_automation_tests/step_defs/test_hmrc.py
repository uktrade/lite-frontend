from pytest_bdd import when, scenarios, parsers

from pages.exporter_hub_page import ExporterHubPage
from pages.hmrc_query.task_list import HMRCQueryTaskListPage
from pages.hmrc_query.find_organisation import HMRCQueryFindOrganisationPage

scenarios("../features/hmrc.feature", strict_gherkin=False)


@when("I select to raise a query for my first organisation")
def raise_query_on_behalf_of_my_first_org(driver, context):
    ExporterHubPage(driver).click_raise_hmrc_query()
    page = HMRCQueryFindOrganisationPage(driver)
    page.search_for_org(context.org_name)
    page.click_org_radio_button(context.org_id)
    page.click_continue()


@when("I click on application hmrc locations link")  # noqa
def i_click_application_locations_link(driver):
    HMRCQueryTaskListPage(driver).click_application_locations_link()


@when("I click on hmrc describe your goods")  # noqa
def i_click_on_hmrc_describe_goods(driver):
    HMRCQueryTaskListPage(driver).click_describe_your_goods()


@when("I click on hmrc set end user")  # noqa
def i_click_on_hmrc_set_end_user(driver):
    HMRCQueryTaskListPage(driver).click_set_end_user()


@when("I click on hmrc explain your reasoning")  # noqa
def i_click_on_hmrc_explain_your_reasoning(driver):
    HMRCQueryTaskListPage(driver).click_explain_your_reasoning()


@when(parsers.parse('I leave a note for the "{reasoning}"'))  # noqa
def i_leave_a_note(driver, reasoning):  # noqa
    text_area = driver.find_element_by_id("reasoning")
    text_area.clear()
    text_area.send_keys(reasoning)
