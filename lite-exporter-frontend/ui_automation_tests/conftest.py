import datetime
import os
import time

from pytest_bdd import given, when, then, parsers
from selenium.webdriver.common.by import By

from pages.add_end_user_pages import AddEndUserPages
from pages.application_edit_type_page import ApplicationEditTypePage
from pages.application_page import ApplicationPage
from pages.open_application.add_goods_type import OpenApplicationAddGoodsType
from pages.respond_to_ecju_query_page import RespondToEcjuQueryPage
from pages.submitted_applications_page import SubmittedApplicationsPages
from shared import functions
from ui_automation_tests.fixtures.env import environment  # noqa
from ui_automation_tests.fixtures.register_organisation import (  # noqa
    register_organisation,
    register_organisation_for_switching_organisation,
    user_details,
)
from ui_automation_tests.fixtures.add_party import add_end_user_to_application  # noqa
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

from ui_automation_tests.shared.fixtures.add_a_draft import add_a_draft  # noqa
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
    exporter_info,
    internal_info,
    seed_data_config,
)
from ui_automation_tests.shared.fixtures.urls import exporter_url, api_url  # noqa

import shared.tools.helpers as utils
from pages.add_goods_page import AddGoodPage
from pages.generic_application.task_list import GenericApplicationTaskListPage
from pages.apply_for_a_licence_page import ApplyForALicencePage
from pages.attach_document_page import AttachDocumentPage
from pages.exporter_hub_page import ExporterHubPage
from pages.hub_page import Hub
from pages.shared import Shared
from pages.sites_page import SitesPage
from pages.which_location_form_page import WhichLocationFormPage

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

        lite_api_url = os.environ.get("LOCAL_LITE_API_URL", os.environ.get("LITE_API_URL"),)

        parser.addoption(
            "--lite_api_url", action="store", default=lite_api_url, help="url",
        )

    elif env == "demo":
        raise Exception("This is the demo environment - Try another environment instead")
    else:
        parser.addoption(
            "--exporter_url",
            action="store",
            default=f"https://exporter.lite.service.{env}.uktrade.digital/",
            help="url",
        )
        parser.addoption(
            "--lite_api_url", action="store", default=f"https://lite-api-{env}.london.cloudapps.digital/", help="url",
        )
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")


def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = "{0}_{1}".format(class_name, "error")
        try:
            utils.save_screenshot(node.funcargs.get("driver"), name)
        except Exception:  # noqa
            pass


@given("I create a standard application via api")  # noqa
def standard_application_exists(apply_for_standard_application):  # noqa
    pass


@given("I create a draft")  # noqa
def create_a_draft(add_a_draft):  # noqa
    pass


@when("my application has been withdrawn")  # noqa
def withdrawn_application_exists(manage_case_status_to_withdrawn):  # noqa
    pass


@when("I click on application previously created")  # noqa
def click_on_an_application(driver, context):  # noqa
    # Works on both the Drafts list and Applications list
    driver.find_element_by_css_selector('a[href*="' + context.app_id + '"]').click()


@when("I go to application previously created")  # noqa
def click_on_an_application(driver, exporter_url, context):  # noqa
    driver.get(exporter_url.rstrip("/") + "/applications/" + context.app_id)


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


def enter_application_name(driver, context):  # noqa
    apply = ApplyForALicencePage(driver)
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id
    app_name = "Request for Nimbus 2000 " + app_time_id
    apply.enter_name_or_reference_for_application(app_name)
    context.app_name = app_name
    functions.click_submit(driver)


def enter_type_of_application(driver, type, context):  # noqa
    context.type = type
    # type needs to be standard or open
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence(type)
    functions.click_submit(driver)


def enter_permanent_or_temporary(driver, permanent_or_temporary, context):  # noqa
    context.perm_or_temp = permanent_or_temporary
    # type needs to be permanent or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_permanent_or_temporary_button(permanent_or_temporary)
    functions.click_submit(driver)


def enter_export_licence(driver, yes_or_no, reference, context):  # noqa
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence_yes_or_no(yes_or_no)
    context.ref = reference
    apply.type_into_reference_number(reference)
    functions.click_submit(driver)


@when("I create a standard application")  # noqa
def create_standard_application(driver, context):  # noqa
    click_apply_licence(driver)
    enter_type_of_application(driver, "standard", context)
    enter_application_name(driver, context)
    enter_permanent_or_temporary(driver, "permanent", context)
    enter_export_licence(driver, "yes", "123456", context)


@when("I click on application locations link")  # noqa
def i_click_application_locations_link(driver):  # noqa
    app = GenericApplicationTaskListPage(driver)
    app.click_application_locations_link()


@when(  # noqa
    parsers.parse(
        'I add an end user of sub_type: "{type}", name: "{name}", website: "{website}", address: "{address}" and country "{'
        'country}"'
    )
)
def add_new_end_user(driver, type, name, website, address, country, context):  # noqa
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.create_new_or_copy_existing(copy_existing=False)
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


@when(  # noqa
    parsers.parse(
        'I add a good with description "{description}" controlled "{controlled}" control code "{control_code}" and part number "{part}"'
    )
)
def add_new_good(driver, description, controlled, control_code, part, context):  # noqa
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


@then("application is submitted")  # noqa
def application_is_submitted(driver):  # noqa
    assert ApplyForALicencePage(driver).is_success_panel_present()


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
    element = GenericApplicationTaskListPage(driver).get_text_of_lite_task_list_items()
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
    assert apply.is_success_panel_present()
    context.time_date_submitted = datetime.datetime.now().strftime("%I:%M%p").lstrip("0").replace(
        " 0", " "
    ).lower() + datetime.datetime.now().strftime(" %d %B %Y")


@when("I click on the manage my organisation link")  # noqa
def click_users_link(driver):  # noqa
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_users()


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


@when("I click the back link")  # noqa
def click_back_link(driver):  # noqa
    functions.click_back_link(driver)


@when("I click the notes tab")  # noqa
def click_notes_tab(driver):  # noqa
    application_page = ApplicationPage(driver)
    application_page.click_notes_tab()


@when("I click the ECJU Queries tab")  # noqa
def click_the_ecju_query_tab(driver):  # noqa
    application_page = ApplicationPage(driver)
    application_page.click_ecju_query_tab()


@when("I click to respond to the ecju query")  # noqa
def respond_to_ecju_click(driver):  # noqa
    application_page = ApplicationPage(driver)
    application_page.respond_to_ecju_query(0)


@when(parsers.parse('I enter "{response}" for ecju query and click submit'))  # noqa
def respond_to_query(driver, response):  # noqa
    response_page = RespondToEcjuQueryPage(driver)
    response_page.enter_form_response(response)
    functions.click_submit(driver)


@then("I see my ecju query is closed")  # noqa
def determine_that_there_is_a_closed_query(driver):  # noqa
    application_page = ApplicationPage(driver)
    closed_queries = application_page.get_count_of_closed_ecju_queries()
    assert closed_queries > 0


@when(parsers.parse('I select "{value}" for submitting response and click submit'))  # noqa
def submit_response_confirmation(driver, value):  # noqa
    driver.find_element_by_xpath('//input[@value="' + value + '"]').click()
    driver.find_element_by_xpath('//button[@type="submit"]').click()


@when(parsers.parse('I enter "{text}" for case note'))  # noqa
def enter_case_note_text(driver, text, context):  # noqa
    application_page = SubmittedApplicationsPages(driver)
    if text == "the maximum limit with spaces":
        text = " " * 2200
    elif text == "the maximum limit":
        text = "T" * 2200
    elif text == "the maximum limit plus 1":
        text = "T" * 2201
    context.text = text
    application_page.enter_case_note(text)


@when("I click post note")  # noqa
def click_post_note(driver, context):  # noqa
    application_page = SubmittedApplicationsPages(driver)
    application_page.click_post_note_btn()


@when(parsers.parse('I upload a file "{filename}"'))  # noqa
def upload_a_file(driver, filename):  # noqa
    attach_document_page = AttachDocumentPage(driver)
    file_path = get_file_upload_path(filename)
    attach_document_page.choose_file(file_path)
    functions.click_submit(driver)


@when("I click on end user")  # noqa
def i_click_on_end_user(driver):  # noqa
    app = GenericApplicationTaskListPage(driver)
    utils.scroll_to_element_by_id(driver, app.END_USER_LINK)
    app.click_end_user_link()


@when("I click on consignees")  # noqa
def i_click_on_consignees(driver):  # noqa
    utils.scroll_to_element_by_id(Shared(driver).driver, "consignees")
    GenericApplicationTaskListPage(driver).click_consignee_link()


@when("I click on activity tab")  # noqa
def activity_tab(driver):  # noqa
    ApplicationPage(driver).click_activity_tab()


@then(parsers.parse('"{expected_text}" is shown as position "{no}" in the audit trail'))  # noqa
def latest_audit_trail(driver, expected_text, no):  # noqa
    assert expected_text in ApplicationPage(driver).get_text_of_audit_trail_item(int(no) - 1)


@when("I wait for document to upload")  # noqa
def wait_for_document(driver):  # noqa
    document_is_found = False
    while not document_is_found:
        if "Processing" in driver.find_element_by_id("document").text:
            time.sleep(1)
            driver.refresh()
        else:
            document_is_found = True


@when("I click on end user advisories")  # noqa
def click_my_end_user_advisory_link(driver):  # noqa
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_end_user_advisories()


@when(  # noqa
    parsers.parse(
        'I add a goods type with description "{description}" controlled "{controlled}" control code "{control_code}" incorporated "{incorporated}"'
    )
)
def add_new_goods_type(driver, description, controlled, control_code, incorporated, context):  # noqa
    OpenApplicationAddGoodsType(driver).enter_description(description)
    OpenApplicationAddGoodsType(driver).select_is_your_good_controlled(controlled)
    OpenApplicationAddGoodsType(driver).enter_control_code(control_code)
    if incorporated != "N/A":
        OpenApplicationAddGoodsType(driver).select_is_your_good_incorporated(incorporated)

    context.good_description = description
    context.control_code = control_code

    functions.click_submit(driver)
