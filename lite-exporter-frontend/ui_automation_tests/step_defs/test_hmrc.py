from pytest_bdd import when, scenarios

from pages.exporter_hub_page import ExporterHubPage
from pages.hmrc_query_page import HMRCQueryPage
from pages.shared import Shared

scenarios('../features/hmrc.feature', strict_gherkin=False)


@when("I select to raise a query for my first organisation")
def raise_query_on_behalf_of_my_first_org(driver, context):
    ExporterHubPage(driver).click_raise_hmrc_query()
    page = HMRCQueryPage(driver)
    page.search_for_org(context.org_name)
    Shared(driver).click_continue()
    page.select_first_org_in_list()
