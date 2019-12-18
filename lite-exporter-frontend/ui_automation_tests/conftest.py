import datetime
import os
import pytest
from pytest_bdd import given, when, then, parsers
from selenium.webdriver.common.by import By

from pages.add_end_user_pages import AddEndUserPages
from pages.application_edit_type_page import ApplicationEditTypePage
from pages.application_page import ApplicationPage
from shared import functions
from ui_automation_tests.fixtures.register_organisation import (  # noqa
    register_organisation,
    register_organisation_for_switching_organisation,
)
from ui_automation_tests.fixtures.env import environment  # noqa
from ui_automation_tests.fixtures.add_goods import (  # noqa
    add_an_incorporated_good_to_application,
    add_a_non_incorporated_good_to_application,
    create_non_incorporated_good,
)
from ui_automation_tests.fixtures.add_clc_query import add_clc_query  # noqa
from ui_automation_tests.fixtures.add_end_user_advisory import add_end_user_advisory  # noqa
from ui_automation_tests.fixtures.internal_ecju_query import (  # noqa
    internal_ecju_query,
    internal_ecju_query_end_user_advisory,
)
from ui_automation_tests.fixtures.sso_sign_in import sso_sign_in  # noqa
from ui_automation_tests.fixtures.internal_case_note import (  # noqa
    internal_case_note,
    internal_case_note_end_user_advisory,
)
from ui_automation_tests.fixtures.manage_case import manage_case_status_to_withdrawn  # noqa

from ui_automation_tests.shared.fixtures.apply_for_application import (  # noqa
    apply_for_standard_application,
    add_an_ecju_query,
    apply_for_open_application,
)
from ui_automation_tests.shared.fixtures.add_a_document_template import (  # noqa
    add_a_document_template,
    get_paragraph_text,
    get_template_id,
    get_licence_template_id,
)
from ui_automation_tests.shared.fixtures.add_a_generated_document import add_a_generated_document  # noqa
from ui_automation_tests.shared.fixtures.driver import driver  # noqa
from ui_automation_tests.shared.fixtures.core import (  # noqa
    context,
    invalid_username,
    exporter_info,
    internal_info,
    seed_data_config,
)
from ui_automation_tests.shared.fixtures.urls import exporter_url, api_url  # noqa

import shared.tools.helpers as utils
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
    env = str(os.environ.get("ENVIRONMENT"))
    if env == "None":
        env = "dev"
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    if env == "local":
        parser.addoption(
            "--exporter_url", action="store", default=f"http://localhost:{str(os.environ.get('PORT'))}/", help="url"
        )

        # Get LITE API URL.
        lite_api_url = os.environ.get("LOCAL_LITE_API_URL", os.environ.get("LITE_API_URL"),)
        parser.addoption(
            "--lite_api_url", action="store", default=lite_api_url, help="url",
        )

    elif env == "demo":
        raise Exception("This is the demo environment - Try another environment instead")
    else:
        parser.addoption(
            "--exporter_url", action="store", default=f"https://exporter.lite.service.{env}.uktrade.io/", help="url",
        )
        parser.addoption(
            "--lite_api_url", action="store", default=f"https://lite-api-{env}.london.cloudapps.digital/", help="url",
        )
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
        except Exception:  # noqa
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


@given("I create a standard application via api")  # noqa
def standard_application_exists(apply_for_standard_application):  # noqa
    pass


@when("my application has been withdrawn")  # noqa
def withdrawn_application_exists(manage_case_status_to_withdrawn):  # noqa
    pass


@when("I click on application previously created")  # noqa
def click_on_an_application(driver, context):  # noqa
    # Works on both the Drafts list and Applications list
    driver.find_element_by_css_selector('a[href*="' + context.app_id + '"]').click()


@when("I click edit application")  # noqa
def i_click_edit_application(driver):  # noqa
    ApplicationPage(driver).click_edit_application_link()


@given("I go to exporter homepage and choose Test Org")  # noqa
def go_to_exporter(driver, register_organisation, sso_sign_in, exporter_url, context):  # noqa
    if "pick-organisation" in driver.current_url:
        no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), context.org_name)
        Shared(driver).click_on_radio_buttons(no)
        functions.click_submit(driver)
    elif Shared(driver).get_text_of_heading() != context.org_name:
        Hub(driver).click_switch_link()
        no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), context.org_name)
        Shared(driver).click_on_radio_buttons(no)
        functions.click_submit(driver)


@when("I go to exporter homepage")  # noqa
def go_to_exporter_when(driver, exporter_url):  # noqa
    driver.get(exporter_url)


@when("I click on apply for a license button")  # noqa
def click_apply_licence(driver):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()


@when("I enter in name for application and continue")  # noqa
def enter_application_name(driver, context):  # noqa
    apply = ApplyForALicencePage(driver)
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id
    app_name = "Request for Nimbus 2000 " + app_time_id
    apply.enter_name_or_reference_for_application(app_name)
    context.app_name = app_name
    functions.click_submit(driver)


@when(parsers.parse('I select "{type}" application and continue'))  # noqa
def enter_type_of_application(driver, type, context):  # noqa
    context.type = type
    # type needs to be standard or open
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence(type)
    functions.click_submit(driver)


@when(parsers.parse('I select "{permanent_or_temporary}" option and continue'))  # noqa
def enter_permanent_or_temporary(driver, permanent_or_temporary, context):  # noqa
    context.perm_or_temp = permanent_or_temporary
    # type needs to be permanent or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_permanent_or_temporary_button(permanent_or_temporary)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I select "{yes_or_no}" for whether I have an export licence and "{reference}" if I have a reference and continue'
    )
)
def enter_export_licence(driver, yes_or_no, reference, context):  # noqa
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence_yes_or_no(yes_or_no)
    context.ref = reference
    apply.type_into_reference_number(reference)
    functions.click_submit(driver)


@when("I click on application locations link")  # noqa
def i_click_application_locations_link(driver):  # noqa
    app = ApplicationOverviewPage(driver)
    app.click_application_locations_link()


@when(parsers.parse('I click on link with id "{link_id}"'))  # noqa
def i_click_on_link_with_id(driver, link_id):  # noqa
    driver.find_element_by_id(link_id).click()


@when(  # noqa
    parsers.parse(
        'I add an end user of sub_type: "{type}", name: "{name}", website: "{website}", address: "{address}" and country "{'
        'country}"'
    )
)
def add_new_end_user(driver, type, name, website, address, country, context):  # noqa
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.select_type(type)
    context.type_end_user = type
    functions.click_submit(driver)
    add_end_user_pages.enter_name(name)
    context.name_end_user = name
    functions.click_submit(driver)
    add_end_user_pages.enter_website(website)
    functions.click_submit(driver)
    add_end_user_pages.enter_address(address)
    context.address_end_user = address
    add_end_user_pages.enter_country(country)
    functions.click_submit(driver)


@when(parsers.parse('I select "{organisation_or_external}" for where my goods are located'))  # noqa
def choose_location_type(driver, organisation_or_external):  # noqa
    which_location_form = WhichLocationFormPage(driver)
    which_location_form.click_on_organisation_or_external_radio_button(organisation_or_external)
    functions.click_submit(driver)


@when(parsers.parse('I select "{choice}" for whether or not I want a new or existing location to be added'))  # noqa
def choose_location_type(driver, choice):  # noqa
    which_location_form = WhichLocationFormPage(driver)
    which_location_form.click_on_choice_radio_button(choice)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I fill in new external location form with name: "{name}", address: "{address}" and country: "{country}" and continue'
    )
)
def add_new_external_location(driver, name, address, country):  # noqa
    add_new_external_location_form_page = AddNewExternalLocationFormPage(driver)
    add_new_external_location_form_page.enter_external_location_name(name)
    add_new_external_location_form_page.enter_external_location_address(address)
    add_new_external_location_form_page.enter_external_location_country(country)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse('I select the location at position "{position_number}" in external locations list and continue')
)
def assert_checkbox_at_position(driver, position_number):  # noqa
    preexisting_locations_page = PreexistingLocationsPage(driver)
    preexisting_locations_page.click_external_locations_checkbox(int(position_number) - 1)
    functions.click_submit(driver)


@then(parsers.parse('I see "{number_of_locations}" locations'))  # noqa
def i_see_a_number_of_locations(driver, number_of_locations):  # noqa
    assert len(driver.find_elements_by_css_selector("tbody tr")) == int(number_of_locations)


@when("I click on add new address")  # noqa
def i_click_on_add_new_address(driver):  # noqa
    external_locations_page = ExternalLocationsPage(driver)
    external_locations_page.click_add_new_address()


@when("I click on preexisting locations")  # noqa
def i_click_add_preexisting_locations(driver):  # noqa
    external_locations_page = ExternalLocationsPage(driver)
    external_locations_page.click_preexisting_locations()


@then(parsers.parse('error message is "{expected_error}"'))  # noqa
def error_message_is(driver, expected_error):  # noqa
    shared = Shared(driver)
    assert shared.is_error_message_displayed()
    assert expected_error in shared.get_text_of_error_messages()


@when(parsers.parse('I select the site at position "{no}"'))  # noqa
def select_the_site_at_position(driver, no):  # noqa
    sites = SitesPage(driver)
    sites.click_sites_checkbox(int(no) - 1)


@when("I click on applications")  # noqa
def click_my_application_link(driver):  # noqa
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_applications()


@when("I click on goods link")  # noqa
def click_my_goods_link(driver):  # noqa
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_my_goods()


@when("I click on standard goods tile")  # noqa
def click_my_goods_link(driver):  # noqa
    exporter_hub = ApplicationOverviewPage(driver)
    exporter_hub.click_standard_goods_link()


@when("I click on open goods tile")  # noqa
def click_my_goods_link(driver):  # noqa
    exporter_hub = ApplicationOverviewPage(driver)
    exporter_hub.click_open_goods_link()


@when("I click on end user advisories")  # noqa
def click_my_end_user_advisory_link(driver):  # noqa
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_end_user_advisories()


@when("I click the add from organisations goods button")  # noqa
def click_add_from_organisation_button(driver):  # noqa
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()


@when("I click add a good button")  # noqa
def click_add_from_organisation_button(driver):  # noqa
    add_goods_page = AddGoodPage(driver)
    add_goods_page.click_add_a_good()


@when(  # noqa
    parsers.parse(
        'I add a good or good type with description "{description}" controlled "{controlled}" control code '
        '"{control_code}" incorporated "{incorporated}" and part number "{part}"'
    )
)
def add_new_good(driver, description, controlled, control_code, incorporated, part, context):  # noqa
    good_part_needed = True
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
    if controlled.lower() == "unsure":
        functions.click_submit(driver)
    else:
        add_goods_page.enter_control_code(control_code)
        functions.click_submit(driver)
    if good_part_needed:
        context.good_id_from_url = driver.current_url.split("/goods/")[1].split("/")[0]


def get_file_upload_path(filename):  # noqa
    # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
    file_to_upload_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "resources", filename))
    if "ui_automation_tests" not in file_to_upload_abs_path:
        file_to_upload_abs_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "ui_automation_tests/resources", filename)
        )
    return file_to_upload_abs_path


@when(parsers.parse('I upload a file "{filename}"'))  # noqa
def upload_a_file(driver, filename):  # noqa
    attach_document_page = AttachDocumentPage(driver)
    file_path = get_file_upload_path(filename)
    attach_document_page.choose_file(file_path)
    functions.click_submit(driver)


@when(parsers.parse('I upload file "{filename}" with description "{description}"'))  # noqa
def upload_a_file_with_description(driver, filename, description):  # noqa
    attach_document_page = AttachDocumentPage(driver)
    file_path = get_file_upload_path(filename)
    attach_document_page.choose_file(file_path)
    attach_document_page.enter_description(description)
    functions.click_submit(driver)


@when(parsers.parse('I raise a clc query control code "{control_code}" description "{description}"'))  # noqa
def raise_clc_query(driver, control_code, description):  # noqa
    raise_clc_query_page = AddGoodPage(driver)
    raise_clc_query_page.enter_control_code_unsure(control_code)
    raise_clc_query_page.enter_control_unsure_details(description)
    functions.click_submit(driver)


@when("I click on the goods link from overview")  # noqa
def click_goods_link_overview(driver):  # noqa
    overview_page = ApplicationOverviewPage(driver)
    overview_page.click_open_goods_link()


@then("application is submitted")  # noqa
def application_is_submitted(driver):  # noqa
    apply = ApplyForALicencePage(driver)
    assert "Application sent successfully" in apply.application_submitted_text()


@then("I see submitted application")  # noqa
def application_is_submitted(driver, context):  # noqa
    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + context.app_time_id + "')]]")

    elements = driver.find_elements_by_css_selector("tr")
    element_number = utils.get_element_index_by_text(elements, context.app_time_id, complete_match=False)
    element_row = elements[element_number].text
    assert "Submitted" in element_row
    assert utils.search_for_correct_date_regex_in_element(element_row)
    assert "0 Goods" or "1 Good" or "2 Goods" in element_row
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Status')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Last updated')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Reference')]]").is_displayed()


@then("I see the application overview")  # noqa
def i_see_the_application_overview(driver, context):  # noqa
    element = ApplicationOverviewPage(driver).get_text_of_lite_task_list_items()
    assert "Reference name" in element
    assert context.app_name in element

    app_id = driver.current_url[-36:]
    context.app_id = app_id


@when("I click applications")  # noqa
def i_click_applications(driver):  # noqa
    hub_page = Hub(driver)
    hub_page.click_applications()


@when("I delete the application")  # noqa
def i_delete_the_application(driver):  # noqa
    apply = ApplyForALicencePage(driver)
    apply.click_delete_application()
    assert "Applications - LITE" in driver.title, (
        "failed to go to Applications list page after deleting application " "from application overview page"
    )


@when("I submit the application")  # noqa
def submit_the_application(driver, context):  # noqa
    apply = ApplyForALicencePage(driver)
    functions.click_submit(driver)
    assert apply.get_text_of_success_message() == "Application sent successfully"
    context.time_date_submitted = datetime.datetime.now().strftime("%I:%M%p").lstrip("0").replace(
        " 0", " "
    ).lower() + datetime.datetime.now().strftime(" %d %B %Y")


@when("I click on the manage my organisation link")  # noqa
def click_users_link(driver):  # noqa
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_users()


@when("I create a standard application")  # noqa
def create_standard_application(driver, context):  # noqa
    click_apply_licence(driver)
    enter_type_of_application(driver, "standard", context)
    enter_application_name(driver, context)
    enter_permanent_or_temporary(driver, "permanent", context)
    enter_export_licence(driver, "yes", "123456", context)


@given("I have a second set up organisation")  # noqa
def set_up_second_organisation(register_organisation_for_switching_organisation):  # noqa
    pass


@when("I switch organisations to my second organisation")  # noqa
def switch_organisations_to_my_second_organisation(driver, context):  # noqa
    Hub(driver).click_switch_link()
    no = utils.get_element_index_by_text(
        Shared(driver).get_radio_buttons_elements(), context.org_name_for_switching_organisations
    )
    Shared(driver).click_on_radio_buttons(no)
    functions.click_submit(driver)


@when("I choose to make major edits")  # noqa
def i_choose_to_make_minor_edits(driver):  # noqa
    application_edit_type_page = ApplicationEditTypePage(driver)
    application_edit_type_page.click_major_edits_radio_button()
    application_edit_type_page.click_change_application_button()


@when("I click continue")  # noqa
@when("I click submit")  # noqa
def i_click_submit_button(driver):  # noqa
    functions.click_submit(driver)


@when(parsers.parse('I leave a note for the "{reasoning}"'))  # noqa
def i_leave_a_note(driver, reasoning):  # noqa
    text_area = driver.find_element_by_id(reasoning)
    text_area.clear()
    text_area.send_keys(reasoning)


@when("I click the back link")  # noqa
def click_back_link(driver):  # noqa
    functions.click_back_link(driver)


@when("I click the notes tab")  # noqa
def click_notes_tab(driver):  # noqa
    application_page = ApplicationPage(driver)
    application_page.click_notes_tab()


@when("I click the ECJU Queries tab")  # noqa
def click_ecju_query_tab(driver):  # noqa
    application_page = ApplicationPage(driver)
    application_page.click_ecju_query_tab()
