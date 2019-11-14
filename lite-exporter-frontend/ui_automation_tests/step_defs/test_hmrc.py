from pytest_bdd import when, scenarios

from pages.application_overview_page import ApplicationOverviewPage
from pages.exporter_hub_page import ExporterHubPage
from pages.hmrc_query_page import HMRCQueryPage

scenarios('../features/hmrc.feature', strict_gherkin=False)


@when("I select to raise a query for my first organisation")
def raise_query_on_behalf_of_my_first_org(driver, context):
    ExporterHubPage(driver).click_raise_hmrc_query()
    page = HMRCQueryPage(driver)
    page.search_for_org(context.org_name)
    page.click_org_radio_button(context.org_id)
    page.click_continue()


@when('I click on application hmrc locations link')  # noqa
def i_click_application_locations_link(driver):
    app = ApplicationOverviewPage(driver)
    app.click_hmrc_application_locations_link()


@when('I click on hmrc describe your goods')  # noqa
def i_click_on_hmrc_describe_goods(driver):
    app = ApplicationOverviewPage(driver)
    app.click_hmrc_describe_your_goods()


@when('I click on hmrc set end user')  # noqa
def i_click_on_hmrc_set_end_user(driver):
    app = ApplicationOverviewPage(driver)
    app.click_hmrc_set_end_user()


@when('I click on hmrc explain your reasoning')  # noqa
def i_click_on_hmrc_explain_your_reasoning(driver):
    app = ApplicationOverviewPage(driver)
    app.click_hmrc_explain_your_reasoning()
