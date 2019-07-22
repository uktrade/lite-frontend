import datetime
import logging
from pytest_bdd import scenarios, given, when, then, parsers, scenarios
import random
from selenium.webdriver.common.by import By
from conftest import context
import helpers.helpers as utils
from pages.exporter_hub import ExporterHub

scenarios('../features/application_setup.feature', strict_gherkin=False)

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I click on apply for a license button')
def click_apply_licence(driver):
    exporter = ExporterHub(driver)
    exporter.click_apply_for_a_licence()


@when('I submit the application')
def submit_the_application(driver):
    exporter = ExporterHub(driver)
    exporter.click_submit_application()
    assert exporter.get_text_of_success_message() == "Application submitted"


@when(parsers.parse('I click add to application for the good at position "{no}"'))
def click_add_to_application_button(driver, no):

    context.goods_name = driver.find_elements_by_css_selector('.lite-card .govuk-heading-s')[int(no)-1].text
    context.part_number = driver.find_elements_by_css_selector('.lite-card .govuk-label')[int(no)-1].text
    driver.find_elements_by_css_selector('a.govuk-button')[int(no)-1].click()


@when('I click on the goods link from overview')
def click_goods_link_overview(driver):
    exporter = ExporterHub(driver)
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    exporter.click_goods_link()


@when(parsers.parse('I add values to my good of "{value}" quantity "{quantity}" and unit of measurement "{unit}"'))
def enter_values_for_good(driver, value, quantity, unit):
    context.quantity = quantity
    context.value = value
    context.unit = unit
    exporter_hub = ExporterHub(driver)
    exporter_hub.add_values_to_good(str(value), str(quantity), unit)


@when('I click overview')
def click_overview(driver):
    exporter_hub = ExporterHub(driver)
    exporter_hub.click_on_overview()


@given('I go to exporter homepage')
def go_to_exporter_given(driver, exporter_url):
    driver.get(exporter_url)


@when('I click on start button')
def click_start_button(driver):
    exporter = ExporterHub(driver)
    exporter.click_start_now_btn()


@when('I enter in name for application and continue')
def enter_application_name(driver):
    exporter = ExporterHub(driver)
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id
    app_name = "Test Application " + app_time_id
    exporter.enter_name_or_reference_for_application(app_name)
    context.app_id = app_name
    exporter.click_save_and_continue()


# utils
@when(parsers.parse('I select "{type}" application and continue'))
def enter_type_of_application(driver, type):
    context.type = type
    # type needs to be standard or temporary
    exporter = ExporterHub(driver)
    exporter.click_export_licence(type)
    exporter.click_continue()


@when(parsers.parse('I select "{permanent_or_temporary}" option and continue'))
def enter_permanent_or_temporary(driver, permanent_or_temporary):
    context.perm_or_temp = permanent_or_temporary
    # type needs to be standard or temporary
    exporter = ExporterHub(driver)
    exporter.click_permanent_or_temporary_button(permanent_or_temporary)
    exporter.click_continue()


@when(parsers.parse(
    'I select "{yes_or_no}" for whether I have an export licence and "{reference}" if I have a reference and continue'))
def enter_export_licence(driver, yes_or_no, reference):
    exporter = ExporterHub(driver)
    exporter.click_export_licence_yes_or_no(yes_or_no)
    context.ref = reference
    exporter.type_into_reference_number(reference)
    exporter.click_continue()


@when('I click on application locations link')
def i_click_application_locations_link(driver):
    exporter = ExporterHub(driver)
    exporter.click_application_locations_link()


@when(parsers.parse('I select "{organisation_or_external}" for where my goods are located'))
def choose_location_type(driver, organisation_or_external):
    exporter = ExporterHub(driver)
    exporter.click_on_organisation_or_external_radio_button(organisation_or_external)
    exporter.click_continue()


@when(parsers.parse('I select the site at position "{no}"'))
def select_the_site_at_position(driver, no):
    exporter = ExporterHub(driver)
    exporter.click_sites_checkbox(int(no) - 1)


@when('I click on goods link')
def click_my_goods_link(driver):
    exporter_hub = ExporterHub(driver)
    exporter_hub.click_goods_link()


@when('I click on goods tile')
def click_my_goods_link(driver):
    exporter_hub = ExporterHub(driver)
    exporter_hub.click_goods_tile()


@when('I click on end user')
def i_click_on_end_user(driver):
    exporter = ExporterHub(driver)
    exporter.click_end_user_link()


@when('I click the add from organisations goods button')
def click_add_from_organisation_button(driver):
    driver.find_element_by_css_selector('.govuk-button[href*="add-preexisting"]').click()


@when(parsers.parse(
    'I add a good with description "{description}" controlled "{controlled}" control code "{controlcode}" incorporated "{incorporated}" and part number "{part}"'))
def add_new_good(driver, description, controlled, controlcode, incorporated, part):
    exporter_hub = ExporterHub(driver)
    good_description = description + str(random.randint(1, 1000))
    good_part = part + str(random.randint(1, 1000))
    context.good_description = good_description
    context.part = good_part
    context.controlcode = controlcode
    exporter_hub.click_add_a_good()
    exporter_hub.enter_description_of_goods(good_description)
    exporter_hub.select_is_your_good_controlled(controlled)
    exporter_hub.enter_control_code(controlcode)
    exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product(incorporated)
    exporter_hub.enter_part_number(good_part)
    exporter_hub.click_save_and_continue()


@when(parsers.parse('I add an end user of type: "{type}", name: "{name}", website: "{website}", address: "{address}" and country "{country}"'))
def add_new_end_user(driver, type, name, website, address, country):
    exporter_hub = ExporterHub(driver)
    exporter_hub.select_end_user_type(type)
    exporter_hub.click_continue()
    exporter_hub.enter_end_user_name(name)
    exporter_hub.click_continue()
    exporter_hub.enter_end_user_website(website)
    exporter_hub.click_continue()
    exporter_hub.enter_end_user_address(address)
    exporter_hub.enter_end_user_country(country)
    exporter_hub.click_continue()


@then('good is added to application')
def good_is_added(driver):
    unit = str(context.unit)
    unit = unit.lower()


@then(parsers.parse('driver title equals "{expected_text}"'))
def assert_title_text(driver, expected_text):
    assert driver.title == expected_text


@then('application is submitted')
def application_is_submitted(driver):
    exporter = ExporterHub(driver)
    assert "Application submitted" in exporter.application_submitted_text()
    # TODO find better way of getting ID.
    url = driver.current_url.replace('/overview/', '')
    context.app_id = url[-36:]
    log.info("Application submitted")
