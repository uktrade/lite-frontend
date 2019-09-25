import datetime
import os
import pytest
from pytest_bdd import given, when, then, parsers
from selenium.webdriver.common.by import By

from fixtures.core import context, driver, invalid_username, exporter_sso_login_info, s3_key # noqa
from fixtures.register_organisation import register_organisation, register_organisation_for_switching_organisation # noqa
from fixtures.add_goods import add_an_incorporated_good_to_application, add_a_non_incorporated_good_to_application, create_non_incorporated_good # noqa
from fixtures.add_an_application import add_an_application # noqa
from fixtures.add_clc_query import add_clc_query # noqa
from fixtures.sso_sign_in import sso_sign_in # noqa
from fixtures.internal_case_note import internal_case_note # noqa
from fixtures.urls import exporter_url, api_url # noqa

import helpers.helpers as utils
from pages.add_goods_page import AddGoodPage
from pages.add_new_external_location_form_page import AddNewExternalLocationFormPage
from pages.application_overview_page import ApplicationOverviewPage
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.attach_document_page import AttachDocumentPage
from pages.exporter_hub_page import ExporterHubPage
from pages.external_locations_page import ExternalLocationsPage
from pages.hub_page import Hub
from pages.preexisting_locations_page import PreexistingLocationsPage
from pages.shared import Shared
from pages.sites_page import SitesPage
from pages.which_location_form_page import WhichLocationFormPage

# from core import strings

strict_gherkin = False


def pytest_addoption(parser):
    env = str(os.environ.get('ENVIRONMENT'))
    if env == 'None':
        env = "dev"
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    if env == 'local':
        parser.addoption("--exporter_url", action="store", default="http://localhost:"+str(os.environ.get('PORT')), help="url")
        parser.addoption("--lite_api_url", action="store", default=str(os.environ.get('LITE_API_URL')), help="url")
    elif env == 'dev2':
        parser.addoption("--exporter_url", action="store", default="https://exporter2.lite.service.dev.uktrade.io/", help="url")
        parser.addoption("--lite_api_url", action="store", default="https://lite-api2-dev.london.cloudapps.digital/", help="url")
    elif env == 'demo':
        raise Exception("This is the demo environment - Try another environment instead")
    else:
        parser.addoption("--exporter_url", action="store", default="https://exporter.lite.service." + env + ".uktrade.io/", help="url")
        parser.addoption("--lite_api_url", action="store", default="https://lite-api-" + env + ".london.cloudapps.digital/", help="url")
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")
    parser.addoption("--email", action="store", default="test@mail.com")
    parser.addoption("--password", action="store", default="password")
    parser.addoption("--first_name", action="store", default="Test")
    parser.addoption("--last_name", action="store", default="User")
    # Load in content strings
    # with open('../../lite-content/lite-exporter-frontend/strings.json') as json_file:
    #     strings.constants = json.load(json_file)


def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = "{0}_{1}".format(class_name, "error")
        try:
            utils.save_screenshot(node.funcargs.get("driver"), name)
        except Exception: # noqa
            pass


@pytest.fixture(scope="module")
def email(request):
    return request.config.getoption("--email")


@pytest.fixture(scope="module")
def password(request):
    return request.config.getoption("--password")


@pytest.fixture(scope="module")
def first_name(request):
    return request.config.getoption("--first_name")


@pytest.fixture(scope="module")
def last_name(request):
    return request.config.getoption("--last_name")


@given('I go to exporter homepage and choose Test Org') # noqa
def go_to_exporter(driver, register_organisation, sso_sign_in, exporter_url, context):
    if 'pick-organisation' in driver.current_url:
        no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), context.org_name)
        Shared(driver).click_on_radio_buttons(no)
        Shared(driver).click_continue()
    elif Shared(driver).get_text_of_heading() != context.org_name:
        Hub(driver).click_switch_link()
        no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), context.org_name)
        Shared(driver).click_on_radio_buttons(no)
        Shared(driver).click_continue()


@when('I go to exporter homepage') # noqa
def go_to_exporter_when(driver, exporter_url):
    driver.get(exporter_url)


@when('I click on apply for a license button') # noqa
def click_apply_licence(driver):
    ExporterHubPage(driver).click_apply_for_a_licence()


@when('I click on start button') # noqa
def click_start_button(driver):
    ApplyForALicencePage(driver).click_start_now_btn()


@when('I enter in name for application and continue') # noqa
def enter_application_name(driver, context):
    apply = ApplyForALicencePage(driver)
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id
    app_name = "Request for Nimbus 2000 " + app_time_id
    apply.enter_name_or_reference_for_application(app_name)
    context.app_name = app_name
    apply.click_save_and_continue()


@when(parsers.parse('I select "{type}" application and continue')) # noqa
def enter_type_of_application(driver, type, context):
    context.type = type
    # type needs to be standard or open
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence(type)
    apply.click_continue()


@when(parsers.parse('I select "{permanent_or_temporary}" option and continue')) # noqa
def enter_permanent_or_temporary(driver, permanent_or_temporary, context):
    context.perm_or_temp = permanent_or_temporary
    # type needs to be permanent or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_permanent_or_temporary_button(permanent_or_temporary)
    apply.click_continue()


@when(parsers.parse('I select "{yes_or_no}" for whether I have an export licence and "{reference}" if I have a reference and continue')) # noqa
def enter_export_licence(driver, yes_or_no, reference, context):
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence_yes_or_no(yes_or_no)
    context.ref = reference
    apply.type_into_reference_number(reference)
    apply.click_continue()


@when('I click on application locations link') # noqa
def i_click_application_locations_link(driver):
    app = ApplicationOverviewPage(driver)
    app.click_application_locations_link()


@when(parsers.parse('I select "{organisation_or_external}" for where my goods are located')) # noqa
def choose_location_type(driver, organisation_or_external):
    which_location_form = WhichLocationFormPage(driver)
    which_location_form.click_on_organisation_or_external_radio_button(organisation_or_external)
    which_location_form.click_continue()


@when(parsers.parse('I fill in new external location form with name: "{name}", address: "{address}" and country: "{country}" and continue')) # noqa
def add_new_external_location(driver, name, address, country):
    add_new_external_location_form_page = AddNewExternalLocationFormPage(driver)
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    add_new_external_location_form_page.enter_external_location_country(country)
    add_new_external_location_form_page.click_continue()


@when(parsers.parse('I select the location at position "{position_number}" in external locations list and continue')) # noqa
def assert_checkbox_at_position(driver, position_number):
    preexisting_locations_page = PreexistingLocationsPage(driver)
    preexisting_locations_page.click_external_locations_checkbox(int(position_number)-1)
    preexisting_locations_page.click_continue()


@then(parsers.parse('I see "{number_of_locations}" locations')) # noqa
def i_see_a_number_of_locations(driver, number_of_locations):
    assert len(driver.find_elements_by_css_selector('.lite-card')) == int(number_of_locations)


@when('I click on add new address') # noqa
def i_click_on_add_new_address(driver):
    external_locations_page = ExternalLocationsPage(driver)
    external_locations_page.click_add_new_address()


@when('I click on preexisting locations') # noqa
def i_click_add_preexisting_locations(driver):
    external_locations_page = ExternalLocationsPage(driver)
    external_locations_page.click_preexisting_locations()


@when('I click continue') # noqa
def i_click_continue(driver):
    driver.find_element_by_css_selector("button[type*='submit']").click()


@then(parsers.parse('error message is "{expected_error}"')) # noqa
def error_message_is(driver, expected_error):
    shared = Shared(driver)
    assert shared.is_error_message_displayed()
    assert expected_error in shared.get_text_of_error_messages()


@when(parsers.parse('I select the site at position "{no}"')) # noqa
def select_the_site_at_position(driver, no):
    sites = SitesPage(driver)
    sites.click_sites_checkbox(int(no)-1)


@when('I click on applications') # noqa
def click_my_application_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_applications()


@when('I click on goods link') # noqa
def click_my_goods_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_my_goods()


@when('I click on goods tile') # noqa
def click_my_goods_link(driver):
    exporter_hub = ApplicationOverviewPage(driver)
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    exporter_hub.click_goods_link()


@when('I click on end user advisories') # noqa
def click_my_end_user_advisory_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_end_user_advisories()


@when('I click the add from organisations goods button') # noqa
def click_add_from_organisation_button(driver):
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()


@when('I click add a good button') # noqa
def click_add_from_organisation_button(driver):
    add_goods_page = AddGoodPage(driver)
    add_goods_page.click_add_a_good()


@when(parsers.parse('I add a good or good type with description "{description}" controlled "{controlled}" control code "{control_code}" incorporated "{incorporated}" and part number "{part}"')) # noqa
def add_new_good(driver, description, controlled, control_code, incorporated, part, context):
    good_part_needed = True
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    date_time = utils.get_current_date_time_string()
    good_description = "%s %s" % (description, date_time)
    good_part = "%s %s" % (part, date_time)
    context.good_description = good_description
    context.part = good_part
    context.control_code = control_code
    add_goods_page.enter_description_of_goods(good_description)
    add_goods_page.select_is_your_good_controlled(controlled)
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product(incorporated)
    if "not needed" in good_part:
        good_part_needed = False
    elif "empty" not in good_part:
        add_goods_page.enter_part_number(good_part)
    if controlled.lower() == 'unsure':
        exporter_hub.click_save_and_continue()
    else:
        add_goods_page.enter_control_code(control_code)
        exporter_hub.click_save_and_continue()
    if good_part_needed:
        context.good_id_from_url = driver.current_url.split('/goods/')[1].split('/')[0]


def get_file_upload_path(filename):
    # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
    file_to_upload_abs_path = \
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'resources', filename))
    if 'ui_automation_tests' not in file_to_upload_abs_path:
        file_to_upload_abs_path = \
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir, 'ui_automation_tests/resources', filename))
    return file_to_upload_abs_path


@when(parsers.parse('I upload a file "{filename}"')) # noqa
def upload_a_file(driver, filename):
    attach_document_page = AttachDocumentPage(driver)
    file_path = get_file_upload_path(filename)
    attach_document_page.choose_file(file_path)
    Shared(driver).click_continue()


@when(parsers.parse('I upload file "{filename}" with description "{description}"')) # noqa
def upload_a_file_with_description(driver, filename, description):
    attach_document_page = AttachDocumentPage(driver)
    file_path = get_file_upload_path(filename)
    attach_document_page.choose_file(file_path)
    attach_document_page.enter_description(description)
    Shared(driver).click_continue()


@when(parsers.parse('I raise a clc query control code "{control_code}" description "{description}"')) # noqa
def raise_clc_query(driver, control_code, description):
    raise_clc_query_page = AddGoodPage(driver)
    raise_clc_query_page.enter_control_code_unsure(control_code)
    raise_clc_query_page.enter_control_unsure_details(description)
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_save_and_continue()


@when('I click on the goods link from overview') # noqa
def click_goods_link_overview(driver):
    overview_page = ApplicationOverviewPage(driver)
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    overview_page.click_goods_link()


@then('application is submitted') # noqa
def application_is_submitted(driver):
    apply = ApplyForALicencePage(driver)
    assert "Application submitted" in apply.application_submitted_text()


@then('I see submitted application') # noqa
def application_is_submitted(driver, context):
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + context.app_time_id + "')]]")

    elements = driver.find_elements_by_css_selector('tr')
    element_number = utils.get_element_index_by_text(elements, context.app_time_id)
    element_row = elements[element_number].text
    assert "Submitted" in element_row
    assert utils.search_for_correct_date_regex_in_element(element_row)
    assert "0 Goods" or "1 Good" or "2 Goods" in element_row
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Status')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Last updated')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Reference')]]").is_displayed()


@then('I see the application overview') # noqa
def i_see_the_application_overview(driver, context):
    element = driver.find_element_by_css_selector(".govuk-table").text
    assert "Name" in element
    assert "Licence type" in element
    assert "Export type" in element
    assert "Reference Number" in element
    assert "Created at" in element
    assert context.type.capitalize() + " Licence" in element
    assert context.perm_or_temp.capitalize() in element
    assert context.ref in element

    # This can break if the minute changes between the five lines of code
    assert utils.search_for_correct_date_regex_in_element(element)

    app_id = driver.current_url[-36:]
    context.app_id = app_id


@when('I click applications') # noqa
def i_click_applications(driver):
    hub_page = Hub(driver)
    hub_page.click_applications()


@when('I delete the application') # noqa
def i_delete_the_application(driver):
    apply = ApplyForALicencePage(driver)
    apply.click_delete_application()
    assert 'Exporter hub - LITE' in driver.title, "failed to go to Exporter Hub page after deleting application from application overview page"


@when('I submit the application') # noqa
def submit_the_application(driver, context):
    apply = ApplyForALicencePage(driver)
    apply.click_submit_application()
    assert apply.get_text_of_success_message() == "Application submitted"
    context.time_date_submitted = datetime.datetime.now().strftime("%I:%M%p").lstrip("0").replace(" 0", " ").lower() \
                                  + datetime.datetime.now().strftime(" %d %B %Y")


@when('I click on the manage my organisation link') # noqa
def click_users_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_users()


@when('I create a standard application') # noqa
def create_standard_application(driver, context):
    click_apply_licence(driver)
    click_start_button(driver)
    enter_application_name(driver, context)
    enter_type_of_application(driver, 'standard', context)
    enter_permanent_or_temporary(driver, 'permanent', context)
    enter_export_licence(driver, 'yes', '123456', context)
