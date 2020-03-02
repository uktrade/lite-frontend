import datetime

from pytest_bdd import scenarios, when, then, parsers

from ui_automation_tests.pages.hub_page import Hub
from ui_automation_tests.pages.new_site_page import NewSite
from ui_automation_tests.pages.site_list_overview_page import SitesListOverview
from ui_automation_tests.pages.site_page import SitePage
from ui_automation_tests.pages.sites_page import SitesPage
from ui_automation_tests.pages.goods_locations_page import GoodsLocationsPage

from ui_automation_tests.pages.shared import Shared

scenarios("../features/sites.feature", strict_gherkin=False)


@when("I click new site")
def click_new_site(driver):
    sites = SitesListOverview(driver)
    sites.click_new_site_link()


@when("I click sites link")
def click_new_site(driver):
    hub = Hub(driver)
    hub.click_sites_link()


@when(
    parsers.parse(
        'I enter in text for new site "{edited}" "{address}" "{postcode}" "{city}" ' '"{region}" and "{country}"'
    )
)
def new_sites_info(driver, edited, address, postcode, city, region, country, context):
    new_site = NewSite(driver)
    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    new_site_name = "Head office" + edited + time_id
    context.new_site_name = new_site_name
    new_site.enter_info_for_new_site(new_site_name, address, postcode, city, region, country)


@then("I see sites list")
def i_see_sites_list(driver, context):
    assert context.new_site_name in Shared(driver).get_text_of_gov_table(), (
        "Failed to return to Sites list page " "after Adding site "
    )


@when("I click the first view link")
def click_first_view_link(driver):
    site_list_overview_page = SitesListOverview(driver)
    site_list_overview_page.click_on_the_view_button_at_first_position()


@when("I click the edit button")
def click_edit_button(driver):
    SitePage(driver).click_edit_button()


@when("I clear the fields for the site")
def clear_site(driver):
    new_site = NewSite(driver)
    new_site.clear_info_for_site()


@then("I see last site name as edited")
def last_site_name_edited(driver, context):
    assert context.new_site_name in Shared(driver).get_text_of_body()


@then(parsers.parse('the checkbox I have selected at position "{no}" is "{checked}"'))
def assert_checkbox_at_position(driver, no, checked):
    sites_page = SitesPage(driver)
    if checked == "checked":
        assert sites_page.get_checked_attribute_of_sites_checkbox(int(no) - 1) == "true"
    elif checked == "unchecked":
        assert sites_page.get_checked_attribute_of_sites_checkbox(int(no) - 1) is not "true"


@when("I click edit sites button")
def i_click_edit_sites_button(driver):
    goods_locations_page = GoodsLocationsPage(driver)
    goods_locations_page.click_edit_sites_button()
