import datetime

from pytest_bdd import scenarios, when, then, parsers

from pages.hub_page import Hub
from pages.new_site_page import NewSite
from pages.site_list_overview_page import SitesListOverview
from pages.sites_page import SitesPage
from pages.goods_locations_page import GoodsLocationsPage

from ui_automation_tests.pages.shared import Shared

scenarios("../features/sites.feature", strict_gherkin=False)


@when("I click new site")
def click_new_site(driver):
    sites = SitesListOverview(driver)
    sites.click_new_sites_link()


@when("I click sites link")
def click_new_site(driver):
    hub = Hub(driver)
    hub.click_sites_link()


@when("I click sites link from overview")
def click_new_site(driver):
    hub = Hub(driver)
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
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


@when("I click the first edit link")
def click_first_edit_link(driver):
    site_list_overview_page = SitesListOverview(driver)
    site_list_overview_page.click_on_the_edit_button_at_first_position()


@when("I clear the fields for the site")
def clear_site(driver):
    new_site = NewSite(driver)
    new_site.clear_info_for_site()


@then("I see last site name as edited")
def last_site_name_edited(driver, context):
    assert context.new_site_name in Shared(driver).get_text_of_gov_table()


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
