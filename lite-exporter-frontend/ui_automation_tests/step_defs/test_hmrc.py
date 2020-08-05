from pytest_bdd import when, scenarios, parsers

from ui_automation_tests.pages.exporter_hub_page import ExporterHubPage
from ui_automation_tests.pages.hmrc_query.find_organisation import HMRCQueryFindOrganisationPage
from ui_automation_tests.pages.open_application.add_goods_type import OpenApplicationAddGoodsType
from ui_automation_tests.shared import functions

scenarios("../features/hmrc.feature", strict_gherkin=False)


@when("I select to raise a query for my first organisation")
def raise_query_on_behalf_of_my_first_org(driver, context):
    ExporterHubPage(driver).click_raise_hmrc_query()
    page = HMRCQueryFindOrganisationPage(driver)
    page.search_for_org(context.org_name)
    page.click_org_radio_button(context.org_id)
    page.click_continue()


@when(parsers.parse('I add a goods type with description "{description}"'))  # noqa
def add_new_goods_type(driver, description, context):  # noqa
    OpenApplicationAddGoodsType(driver).enter_description(description)
    context.good_description = description

    functions.click_submit(driver)


@when(parsers.parse('I leave a note for the "{reasoning}"'))  # noqa
def i_leave_a_note(driver, reasoning):  # noqa
    text_area = driver.find_element_by_id("reasoning")
    text_area.clear()
    text_area.send_keys(reasoning)
