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
from pages.standard_application.task_list import StandardApplicationTaskListPage
from pages.standard_application.good_details import StandardApplicationGoodDetails
from pages.standard_application.goods import StandardApplicationGoodsPage
from pages.add_new_external_location_form_page import AddNewExternalLocationFormPage
from shared import functions
from shared.tools.wait import wait_for_element, wait_for_download_button

from ui_automation_tests.fixtures.env import environment  # noqa
from ui_automation_tests.fixtures.register_organisation import (  # noqa
    register_organisation,
    register_organisation_for_switching_organisation,
)
from ui_automation_tests.fixtures.add_party import add_end_user_to_application  # noqa
from ui_automation_tests.fixtures.add_goods_query import add_goods_clc_query  # noqa
from ui_automation_tests.fixtures.add_end_user_advisory import add_end_user_advisory  # noqa
from ui_automation_tests.fixtures.sso_sign_in import sso_sign_in  # noqa
from ui_automation_tests.fixtures.manage_case import manage_case_status_to_withdrawn, approve_case  # noqa
from ui_automation_tests.shared.fixtures.add_a_draft import add_a_draft  # noqa
from ui_automation_tests.shared.fixtures.apply_for_application import (  # noqa
    apply_for_standard_application,
    add_an_ecju_query,
    apply_for_open_application,
    apply_for_exhibition_clearance,
    apply_for_f680_clearance,
    apply_for_gifting_clearance,
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
    api_client_config,
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
from ui_automation_tests.pages.add_goods_grading_page import AddGoodGradingPage

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


@when("I enter a licence name")  # noqa
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


def select_goods_categories(driver):  # noqa
    apply = ApplyForALicencePage(driver)
    assert len(driver.find_elements_by_name(apply.CHECKBOXES_GOODS_CATEGORIES_NAME)) == 4
    apply.select_goods_categories()
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
    ApplyForALicencePage(driver).select_licence_type("export_licence")
    functions.click_submit(driver)
    enter_type_of_application(driver, "standard", context)
    enter_application_name(driver, context)
    enter_permanent_or_temporary(driver, "permanent", context)
    select_goods_categories(driver)
    enter_export_licence(driver, "yes", "123456", context)


@when(parsers.parse('I select a licence of type "{type}"'))  # noqa
def create_mod_application(driver, context, type):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    ApplyForALicencePage(driver).select_licence_type(type)
    functions.click_submit(driver)


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


@when(parsers.parse('I select "{choice}" for where my goods are located'))  # noqa
def choose_location_type(driver, choice):  # noqa
    which_location_form = WhichLocationFormPage(driver)
    which_location_form.click_on_location_radiobutton(choice)
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
        'I add a good with description "{description}" part number "{part}" controlled "{controlled}" control code "{control_code}" and graded "{graded}"'
    )
)
def add_new_good(driver, description, part, controlled, control_code, graded, context):  # noqa
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
    if controlled.lower() == "yes":
        add_goods_page.enter_control_code(control_code)
    if good_part_needed:
        context.good_id_from_url = driver.current_url.split("/goods/")[1].split("/")[0]
    add_goods_page.select_is_your_good_graded(graded)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I add the goods grading with prefix "{prefix}" grading "{grading}" suffix "{suffix}" '
        'issuing authority "{issuing_authority}" reference "{reference}" Date of issue "{date_of_issue}"'
    )
)
def add_good_grading(driver, prefix, grading, suffix, issuing_authority, reference, date_of_issue, context):  # noqa
    goods_grading_page = AddGoodGradingPage(driver)
    goods_grading_page.enter_prefix_of_goods_grading(prefix)
    goods_grading_page.enter_good_grading(grading)
    goods_grading_page.enter_suffix_of_goods_grading(suffix)
    goods_grading_page.enter_issuing_authority(issuing_authority)
    goods_grading_page.enter_reference(reference)
    date = date_of_issue.split("-")
    goods_grading_page.enter_date_of_issue(date[0], date[1], date[2])
    functions.click_submit(driver)


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


@then("I see the application overview")  # noqa
def i_see_the_application_overview(driver, context):  # noqa
    element = GenericApplicationTaskListPage(driver).get_text_of_lite_task_list_items()
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
    utils.scroll_to_element_by_id(driver, app.LINK_END_USER_ID)
    app.click_end_user_link()


@when("I click on consignees")  # noqa
def i_click_on_consignees(driver):  # noqa
    app = GenericApplicationTaskListPage(driver)
    utils.scroll_to_element_by_id(Shared(driver).driver, app.LINK_CONSIGNEE_ID)
    app.click_consignee_link()


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
    OpenApplicationAddGoodsType(driver).select_is_your_good_incorporated(incorporated)

    context.good_description = description
    context.control_code = control_code

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


@when("I click on goods")  # noqa
def i_click_on_goods(driver):  # noqa
    StandardApplicationTaskListPage(driver).click_goods_link()


@when("I add a non-incorporated good to the application")  # noqa
def i_add_a_non_incorporated_good_to_the_application(driver, context):  # noqa
    StandardApplicationGoodsPage(driver).click_add_preexisting_good_button()

    # Click the "Add to application" link on the first good
    driver.find_elements_by_css_selector(".govuk-table__row .govuk-link")[0].click()

    # Enter good details
    StandardApplicationGoodDetails(driver).enter_value("1")
    StandardApplicationGoodDetails(driver).enter_quantity("2")
    StandardApplicationGoodDetails(driver).select_unit("Number of articles")
    StandardApplicationGoodDetails(driver).check_is_good_incorporated_false()
    context.is_good_incorporated = "No"

    functions.click_submit(driver)


@then("the good is added to the application")  # noqa
def the_good_is_added_to_the_application(driver, context):  # noqa
    body_text = Shared(driver).get_text_of_body()

    assert len(StandardApplicationGoodsPage(driver).get_goods()) == 1  # Only one good added
    assert StandardApplicationGoodsPage(driver).get_goods_total_value() == "£1.00"  # Value
    assert "2.0" in body_text  # Quantity
    assert "Number of articles" in body_text  # Unit
    assert context.is_good_incorporated in body_text  # Incorporated

    # Go back to task list
    functions.click_back_link(driver)


@then("wait for download link")  # noqa
def wait_for_download_link(driver):  # noqa
    assert wait_for_download_button(driver, page=Shared(driver))


@then(parsers.parse('Wait for "{element_id}" to be present'))  # noqa
def wait_for_element_to_be_present(driver, element_id):  # noqa
    assert wait_for_element(driver, element_id)


@when("I change my reference name")  # noqa
def change_ref_name(driver, context):  # noqa
    driver.find_element_by_id("link-reference-name").click()
    enter_application_name(driver, context)


@then("I see my edited reference name")
def assert_ref_name(context, driver):  # noqa
    assert context.app_name in driver.find_element_by_css_selector(".lite-task-list").text


@then("I see my edited reference number")
def assert_ref_num(driver):  # noqa
    assert "12345678" in driver.find_element_by_css_selector(".lite-task-list").text


@when("I change my reference number")
def change_ref_num(driver, context):  # noqa
    driver.find_element_by_id("link-told-by-an-official").click()
    enter_export_licence(driver, "yes", "12345678", context)


@when("I remove a good from the application")
def i_remove_a_good_from_the_application(driver):  # noqa
    GenericApplicationTaskListPage(driver).get_remove_good_link().click()


@then("the good has been removed from the application")
def no_goods_are_left_on_the_application(driver):  # noqa
    assert not functions.element_with_css_selector_exists(
        driver, GenericApplicationTaskListPage(driver).REMOVE_GOOD_LINK
    )


@when("I remove the end user off the application")
def i_remove_the_end_user_off_the_application(driver):  # noqa
    GenericApplicationTaskListPage(driver).click_end_user_link()
    remove_end_user_link = GenericApplicationTaskListPage(driver).find_remove_end_user_link()
    driver.execute_script("arguments[0].click();", remove_end_user_link)
    functions.click_back_link(driver)


@then("no end user is set on the application")
def no_end_user_is_set_on_the_application(driver):  # noqa
    assert not GenericApplicationTaskListPage(driver).does_remove_end_user_exist(driver)


@when("I remove the consignee off the application")
def i_remove_the_consignee_off_the_application(driver):  # noqa
    GenericApplicationTaskListPage(driver).click_consignee_link()
    remove_consignee_link = GenericApplicationTaskListPage(driver).find_remove_consignee_link()
    driver.execute_script("arguments[0].click();", remove_consignee_link)
    functions.click_back_link(driver)


@then("no consignee is set on the application")
def no_consignee_is_set_on_the_application(driver):  # noqa
    assert not GenericApplicationTaskListPage(driver).does_remove_consignee_exist(driver)


@when("I click on the application third parties link")
def i_click_on_application_third_parties_link(driver):  # noqa
    StandardApplicationTaskListPage(driver).click_third_parties_link()


@when("I remove a third party from the application")
def i_remove_a_third_party_from_the_application(driver):  # noqa
    remove_good_link = GenericApplicationTaskListPage(driver).find_remove_third_party_link()
    driver.execute_script("arguments[0].click();", remove_good_link)
    functions.click_back_link(driver)


@then("the third party has been removed from the application")
def no_third_parties_are_left_on_the_application(driver):  # noqa
    assert not functions.element_with_css_selector_exists(
        driver, GenericApplicationTaskListPage(driver).REMOVE_THIRD_PARTY_LINK
    )


@when("I remove an additional document")
def i_remove_an_additional_document(driver):  # noqa
    driver.set_timeout_to(0)
    GenericApplicationTaskListPage(driver).click_supporting_documents_link()
    remove_additional_document_link = GenericApplicationTaskListPage(driver).find_remove_additional_document_link()
    driver.set_timeout_to(10)
    driver.execute_script("arguments[0].click();", remove_additional_document_link)


@when("I confirm I want to delete the document")
def i_click_confirm(driver):  # noqa
    GenericApplicationTaskListPage(driver).confirm_delete_additional_document()


@then("the document is removed from the application")
def no_documents_are_set_on_the_application(driver):  # noqa
    assert not GenericApplicationTaskListPage(driver).does_remove_additional_document_exist(driver)
