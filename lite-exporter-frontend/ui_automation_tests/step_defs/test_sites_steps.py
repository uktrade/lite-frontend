from pytest_bdd import scenarios, given, when, then, parsers
from pages.site_list_overview_page import SitesListOverview
from pages.new_site_page import NewSite
from pages.sites_page import SitesPage
from pages.shared import Shared
from pages.hub_page import Hub
import datetime
import helpers.helpers as utils
from selenium.webdriver.common.by import By
from conftest import context

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

scenarios('../features/sites.feature', strict_gherkin=False)


@when('I click new site')
def click_new_site(driver):
    sites = SitesListOverview(driver)
    sites.click_new_sites_link()


@when('I click sites link')
def click_new_site(driver):
    hub = Hub(driver)
    hub.click_sites_link()


@when('I click sites link from overview')
def click_new_site(driver):
    hub = Hub(driver)
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    hub.click_sites_link()


@when(parsers.parse('I enter in text for new site "{edited}" {address}" "{postcode}" "{city}" "{region}" and "{country}"'))
def new_sites_info(driver, edited, address, postcode, city, region, country):
    new_site = NewSite(driver)
    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    new_site_name = "New Site " + edited + time_id
    context.new_site_name = new_site_name
    new_site.enter_info_for_new_site(new_site_name, address, postcode, city, region, country)


@then('I see sites list')
def i_see_sites_list(driver):
    assert driver.find_element_by_tag_name("h1").text == "Sites", \
        "Failed to return to Sites list page after Adding site"

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'"+context.new_site_name+"')]]")


@when('I click last edit button')
def click_new_site(driver):
    site_list_overview_page = SitesListOverview(driver)
    site_list_overview_page.click_on_the_edit_button_at_last_position()


@when('I clear the fields for the site')
def clear_site(driver):
    new_site = NewSite(driver)
    new_site.clear_info_for_site()


@then('I see select a site error message')
def select_a_site_error(driver):
    shared = Shared(driver)
    assert "You have to pick at least one site." in shared.get_text_of_error_message()


@then('I see my new site at first position')
def assert_site_is_added_to_list(driver):
    sites_page = SitesPage(driver)
    assert sites_page.get_text_of_site(sites_page.get_size_of_sites()-1) == context.new_site_name


@then('I see last site name as edited')
def last_site_name_edited(driver):
    site_list_overview_page = SitesListOverview(driver)
    assert "edited" in site_list_overview_page.get_text_of_last_site_name()


@then(parsers.parse('the checkbox I have selected at position "{no}" is "{checked}"'))
def assert_checkbox_at_position(driver, no, checked):
    sites_page = SitesPage(driver)
    if checked== "checked":
        assert sites_page.get_checked_attribute_of_sites_checkbox(int(no)-1) == "true"
    elif checked== "unchecked":
        assert sites_page.get_checked_attribute_of_sites_checkbox(int(no)-1) is not "true"
