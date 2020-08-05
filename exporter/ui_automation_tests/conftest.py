import datetime
import os

from django.conf import settings
from faker import Faker  # noqa
import logging
from pytest_bdd import given, when, then, parsers

import ui_automation_tests.shared.tools.helpers as utils
from ui_automation_tests.fixtures.add_end_user_advisory import add_end_user_advisory  # noqa
from ui_automation_tests.fixtures.add_goods_query import add_goods_clc_query  # noqa
from ui_automation_tests.fixtures.add_party import add_end_user_to_application  # noqa
from ui_automation_tests.fixtures.env import environment  # noqa
from ui_automation_tests.fixtures.manage_case import manage_case_status_to_withdrawn, approve_case  # noqa
from ui_automation_tests.fixtures.register_organisation import (  # noqa
    register_organisation,
    register_organisation_for_switching_organisation,
)
from ui_automation_tests.fixtures.sso_sign_in import sso_sign_in  # noqa
from ui_automation_tests.pages.add_end_user_pages import AddEndUserPages
from ui_automation_tests.pages.application_edit_type_page import ApplicationEditTypePage
from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_automation_tests.pages.attach_document_page import AttachDocumentPage
from ui_automation_tests.pages.end_use_details_form_page import EndUseDetailsFormPage
from ui_automation_tests.pages.exporter_hub_page import ExporterHubPage
from ui_automation_tests.pages.generic_application.additional_documents import AdditionalDocumentsPage
from ui_automation_tests.pages.generic_application.declaration import DeclarationPage
from ui_automation_tests.pages.generic_application.task_list import TaskListPage
from ui_automation_tests.pages.hub_page import Hub
from ui_automation_tests.pages.mod_clearances.ExhibitionClearanceDetails import ExhibitionClearanceDetailsPage
from ui_automation_tests.pages.open_application.add_goods_type import OpenApplicationAddGoodsType
from ui_automation_tests.pages.respond_to_ecju_query_page import RespondToEcjuQueryPage
from ui_automation_tests.pages.route_of_goods_form_page import RouteOfGoodsFormPage
from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.pages.sites_page import SitesPage
from ui_automation_tests.pages.standard_application.good_details import StandardApplicationGoodDetails
from ui_automation_tests.pages.standard_application.goods import StandardApplicationGoodsPage
from ui_automation_tests.pages.submitted_applications_page import SubmittedApplicationsPages
from ui_automation_tests.pages.temporary_export_details_form_page import TemporaryExportDetailsFormPage
from ui_automation_tests.pages.which_location_form_page import WhichLocationFormPage
from ui_automation_tests.shared import functions
from ui_automation_tests.shared.fixtures.add_a_document_template import (  # noqa
    add_a_document_template,
    get_paragraph_text,
    get_template_id,
    get_licence_template_id,
)
from ui_automation_tests.shared.fixtures.add_a_draft import add_a_draft  # noqa
from ui_automation_tests.shared.fixtures.add_a_generated_document import add_a_generated_document  # noqa
from ui_automation_tests.shared.fixtures.apply_for_application import (  # noqa
    apply_for_standard_application,
    add_an_ecju_query,
    apply_for_open_application,
    apply_for_exhibition_clearance,
    apply_for_f680_clearance,
    apply_for_gifting_clearance,
    apply_for_standard_trade_control_application,
    apply_for_ogel,
)
from ui_automation_tests.shared.fixtures.core import (  # noqa
    context,
    exporter_info,
    internal_info,
    api_client,
    api_test_client,
)
from ui_automation_tests.shared.fixtures.driver import driver  # noqa
from ui_automation_tests.shared.fixtures.urls import exporter_url, api_url  # noqa
from ui_automation_tests.shared.tools.wait import wait_for_download_button_on_exporter_main_content

strict_gherkin = False
fake = Faker()


def pytest_addoption(parser):
    settings.configure(
        DIRECTORY_SSO_API_CLIENT_API_KEY=os.environ.get("DIRECTORY_SSO_API_CLIENT_API_KEY"),
        DIRECTORY_SSO_API_CLIENT_BASE_URL=os.environ.get("DIRECTORY_SSO_API_CLIENT_BASE_URL"),
        DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT=30,
        DIRECTORY_SSO_API_CLIENT_SENDER_ID="directory",
    )
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
        class_name = (
            node._nodeid.replace(".py::", "").replace("ui_automation_tests/step_defs/", "").replace("step_defs", "")
        )
        name = "{0}_{1}".format(class_name, "").replace("/", "").replace("test", "_test")
        logging.info("Test that has failed is file: %s", name)
        try:
            utils.save_screenshot(node.funcargs.get("driver"), name)
        except Exception as e:  # noqa
            logging.error("Screenshot failed to be taken %e", e)


@given("I create a standard application via api")  # noqa
def standard_application_exists(apply_for_standard_application):  # noqa
    pass


@given("I create an open application via api")  # noqa
def open_application_exists(apply_for_open_application):  # noqa
    pass


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
    elif Shared(driver).get_text_of_organisation_heading() != context.org_name:
        Hub(driver).click_switch_link()
        no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), context.org_name)
        Shared(driver).click_on_radio_buttons(no)
        functions.click_submit(driver)


@when("I go to exporter homepage")  # noqa
def go_to_exporter_when(driver, exporter_url):  # noqa
    driver.get(exporter_url)


@when("I enter a licence name")  # noqa
def enter_application_name(driver, context):  # noqa
    apply = ApplyForALicencePage(driver)
    app_name = fake.bs()
    apply.enter_name_or_reference_for_application(app_name)
    context.app_name = app_name
    functions.click_submit(driver)


def choose_open_licence_category(driver, type_of_oiel, context):  # noqa
    # Values allowed: cryptographic, media, military, uk_continental_shelf, dealer
    apply = ApplyForALicencePage(driver)
    apply.select_open_licence_category(type_of_oiel)


def enter_type_of_application(driver, _type, context):  # noqa
    context.type = _type
    # type needs to be standard or open
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence(_type)
    functions.click_submit(driver)


def enter_permanent_or_temporary(driver, permanent_or_temporary, context):  # noqa
    context.perm_or_temp = permanent_or_temporary
    # type needs to be permanent or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_permanent_or_temporary_button(permanent_or_temporary)
    functions.click_submit(driver)


def answer_firearms_question(driver):  # noqa
    apply = ApplyForALicencePage(driver)
    apply.select_firearms_yes()
    functions.click_submit(driver)


def enter_export_licence(driver, yes_or_no, reference, context):  # noqa
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence_yes_or_no(yes_or_no)
    context.ref = reference
    apply.type_into_reference_number(reference)
    functions.click_submit(driver)


@when(  # noqa
    parsers.parse(
        'I add a party of sub_type: "{type}", name: "{name}", website: "{website}", address: "{address}" and country "{'
        'country}"'
    )
)
def add_new_party(driver, type, name, website, address, country, context):  # noqa
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


@when(parsers.parse('I click on the "{section}" section'))  # noqa
def go_to_task_list_section(driver, section):  # noqa
    TaskListPage(driver).click_on_task_list_section(section)


@when(parsers.parse("I provide details of the intended end use of the products"))  # noqa
def intended_end_use_details(driver):  # noqa
    end_use_details = EndUseDetailsFormPage(driver)
    end_use_details.answer_intended_end_use_details(fake.sentence(nb_words=30))
    functions.click_submit(driver)


@when(parsers.parse('I answer "{choice}" for informed by ECJU to apply'))  # noqa
def military_end_use_details(driver, choice):  # noqa
    end_use_details = EndUseDetailsFormPage(driver)
    if choice == "Yes":
        end_use_details.answer_military_end_use_controls(True, fake.ean(length=13))
    else:
        end_use_details.answer_military_end_use_controls(False)
    functions.click_submit(driver)


@when(parsers.parse('I answer "{choice}" for informed by ECJU about WMD use'))  # noqa
def informed_wmd_end_use_details(driver, choice):  # noqa
    end_use_details = EndUseDetailsFormPage(driver)
    if choice == "Yes":
        end_use_details.answer_is_informed_wmd(True, fake.ean(length=13))
    else:
        end_use_details.answer_is_informed_wmd(False)
    functions.click_submit(driver)


@when(parsers.parse('I answer "{choice}" for suspected WMD use'))  # noqa
def suspected_wmd_end_use_details(driver, choice):  # noqa
    end_use_details = EndUseDetailsFormPage(driver)
    if choice == "Yes":
        end_use_details.answer_is_suspected_wmd(True, fake.sentence(nb_words=30))
    else:
        end_use_details.answer_is_suspected_wmd(False)
    functions.click_submit(driver)


@when(parsers.parse('I answer "{choice}" for shipping air waybill or lading'))  # noqa
def route_of_goods(driver, choice):  # noqa
    route_of_goods = RouteOfGoodsFormPage(driver)
    if choice == "No":
        route_of_goods.answer_route_of_goods_question(True, "Not shipped air waybill.")
    else:
        route_of_goods.answer_route_of_goods_question(False)


@when(parsers.parse("I save and continue on the summary page"))  # noqa
def save_continue_summary_list(driver):  # noqa
    element = driver.find_element_by_css_selector("button[value='finish']")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)


@when("I provide details of why my export is temporary")  # noqa
def enter_temporary_export_details(driver):  # noqa
    temporary_export_details = TemporaryExportDetailsFormPage(driver)
    temporary_export_details.answer_temp_export_details(fake.sentence(nb_words=30))
    functions.click_submit(driver)


@when(parsers.parse('I answer "{choice}" for whether the products remain under my direct control'))  # noqa
def temporary_export_direct_control(driver, choice):  # noqa
    temporary_export_details = TemporaryExportDetailsFormPage(driver)
    if choice == "Yes":
        temporary_export_details.answer_is_temp_direct_control(True)
    else:
        temporary_export_details.answer_is_temp_direct_control(False, fake.sentence(nb_words=30))
    functions.click_submit(driver)


@when(parsers.parse('I enter the date "{day}", "{month}", "{year}" when the products will return to the UK'))  # noqa
def enter_proposed_return_date(driver, day, month, year):  # noqa
    temporary_export_details = TemporaryExportDetailsFormPage(driver)
    temporary_export_details.proposed_return_date(day, month, year)
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


@then("application is submitted")  # noqa
def application_is_submitted(driver):  # noqa
    assert ApplyForALicencePage(driver).is_success_panel_present()


@then("I see submitted application")  # noqa
def application_is_submitted(driver, context):  # noqa

    elements = driver.find_elements_by_css_selector("tr")
    element_number = utils.get_element_index_by_text(elements, context.app_name, complete_match=False)
    element_row = elements[element_number].text
    assert utils.search_for_correct_date_regex_in_element(element_row)
    assert "0 Goods" or "1 Good" or "2 Goods" in element_row
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Status')]]").is_displayed()
    assert driver.find_element_by_xpath("// th[text()[contains(., 'Last updated')]]").is_displayed()


@when("I submit the application")  # noqa
def submit_the_application(driver, context):  # noqa
    functions.click_submit(driver)
    context.time_date_submitted = datetime.datetime.now().strftime("%I:%M%p").lstrip("0").replace(
        " 0", " "
    ).lower() + datetime.datetime.now().strftime(" %d %B %Y")


@when("I click on the manage my organisation link")  # noqa
def click_users_link(driver):  # noqa
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_manage_my_organisation_tile()


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


@when("I choose a clearance level for my application")  # noqa
def choose_application_clearance_level(driver, context):  # noqa
    no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), "uk_unclassified")

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
    # TODO get rid of this xpaths
    driver.find_element_by_xpath('//input[@value="' + value + '"]').click()
    driver.find_element_by_xpath('//button[@type="submit"]').click()


@when(parsers.parse("I enter text for case note"))  # noqa
def enter_case_note_text(driver, context):  # noqa
    application_page = SubmittedApplicationsPages(driver)
    context.text = fake.catch_phrase()
    application_page.enter_case_note(context.text)


@when("I click post note")  # noqa
def click_post_note(driver):  # noqa
    application_page = SubmittedApplicationsPages(driver)
    application_page.click_post_note_button()


@when(parsers.parse('I upload a file "{filename}"'))  # noqa
def upload_a_file(driver, filename):  # noqa
    attach_document_page = AttachDocumentPage(driver)
    file_path = get_file_upload_path(filename)
    attach_document_page.choose_file(file_path)
    functions.click_submit(driver)


@when("I click on activity tab")  # noqa
def activity_tab(driver):  # noqa
    ApplicationPage(driver).click_activity_tab()


@then(parsers.parse('"{expected_text}" is shown as position "{no}" in the audit trail'))  # noqa
def latest_audit_trail(driver, expected_text, no):  # noqa
    assert expected_text.lower() in ApplicationPage(driver).get_text_of_audit_trail_item(int(no) - 1).lower()


@when("I click on end user advisories")  # noqa
def click_my_end_user_advisory_link(driver):  # noqa
    ExporterHubPage(driver).click_end_user_advisories()


@when(  # noqa
    parsers.parse(
        'I add a goods type with description "{description}" controlled "{controlled}" control code "{control_code}" incorporated "{incorporated}"'
    )
)
def add_new_goods_type(driver, description, controlled, control_code, incorporated, context):  # noqa
    OpenApplicationAddGoodsType(driver).enter_description(description)
    OpenApplicationAddGoodsType(driver).select_is_your_good_controlled(controlled)
    OpenApplicationAddGoodsType(driver).enter_control_list_entry(control_code)
    OpenApplicationAddGoodsType(driver).select_is_your_good_incorporated(incorporated)

    context.good_description = description
    context.control_code = control_code

    functions.click_submit(driver)


@when("I add a non-incorporated good to the application")  # noqa
def i_add_a_non_incorporated_good_to_the_application(driver, context):  # noqa
    goods_page = StandardApplicationGoodsPage(driver)
    goods_page.click_add_preexisting_good_button()
    goods_page.click_add_to_application()

    # Enter good details
    goods_details_page = StandardApplicationGoodDetails(driver)
    goods_details_page.enter_value("1")
    goods_details_page.enter_quantity("2")
    goods_details_page.select_unit("Number of articles")
    goods_details_page.check_is_good_incorporated_false()
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


@then("download link is present")  # noqa
def wait_for_download_link(driver):  # noqa
    assert wait_for_download_button_on_exporter_main_content(driver)


@then("I see my edited reference name")
def assert_ref_name(context, driver):  # noqa
    assert context.app_name in driver.find_element_by_css_selector(".lite-task-list").text


@when("I remove a good from the application")
def i_remove_a_good_from_the_application(driver):  # noqa
    StandardApplicationGoodsPage(driver).get_remove_good_link().click()


@then("the good has been removed from the application")
def no_goods_are_left_on_the_application(driver):  # noqa
    assert not StandardApplicationGoodsPage(driver).goods_exist_on_the_application()


@when("I remove the end user off the application")
def i_remove_the_end_user_off_the_application(driver):  # noqa
    remove_end_user_link = TaskListPage(driver).find_remove_party_link()
    driver.execute_script("arguments[0].click();", remove_end_user_link)
    functions.click_back_link(driver)


@then("no end user is set on the application")
def no_end_user_is_set_on_the_application(driver):  # noqa
    assert not TaskListPage(driver).find_remove_party_link()


@when("I remove the consignee off the application")
def i_remove_the_consignee_off_the_application(driver):  # noqa
    remove_consignee_link = TaskListPage(driver).find_remove_party_link()
    driver.execute_script("arguments[0].click();", remove_consignee_link)
    functions.click_back_link(driver)


@then("no consignee is set on the application")
def no_consignee_is_set_on_the_application(driver):  # noqa
    assert not TaskListPage(driver).find_remove_party_link()


@when("I remove a third party from the application")
def i_remove_a_third_party_from_the_application(driver):  # noqa
    remove_good_link = TaskListPage(driver).find_remove_party_link()
    driver.execute_script("arguments[0].click();", remove_good_link)
    functions.click_back_link(driver)


@then("the third party has been removed from the application")
def no_third_parties_are_left_on_the_application(driver):  # noqa
    assert not TaskListPage(driver).find_remove_party_link()


@then("the document has been removed from the application")
def no_documents_are_left_on_the_application(driver):  # noqa
    assert not TaskListPage(driver).find_remove_party_link()


@when("I remove an additional document")
def i_remove_an_additional_document(driver):  # noqa
    remove_additional_document_link = AdditionalDocumentsPage(driver).find_remove_additional_document_link()
    driver.execute_script("arguments[0].click();", remove_additional_document_link)


@when("I confirm I want to delete the document")
def i_click_confirm(driver):  # noqa
    AdditionalDocumentsPage(driver).confirm_delete_additional_document()


@when(parsers.parse('I enter Exhibition details with the name "{name}"'))
def enter_exhibition_details(driver, name):  # noqa
    exhibition_details_page = ExhibitionClearanceDetailsPage(driver)
    exhibition_details_page.enter_exhibition_name(name)
    exhibition_details_page.enter_exhibition_start_date("1", "1", "2100")
    exhibition_details_page.enter_exhibition_required_by_date("1", "1", "2100")
    functions.click_submit(driver)


@then(parsers.parse('The "{section}" section is set to status "{status}"'))  # noqa
def go_to_task_list_section(driver, section, status):  # noqa
    assert TaskListPage(driver).get_section_status(section) == status


def get_file_upload_path(filename):  # noqa
    # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
    file_to_upload_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "resources", filename))
    if "ui_automation_tests" not in file_to_upload_abs_path:
        file_to_upload_abs_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "ui_automation_tests/resources", filename)
        )
    return file_to_upload_abs_path


@when("I agree to the declaration")
def agree_to_the_declaration(driver):  # noqa
    declaration_page = DeclarationPage(driver)
    declaration_page.agree_to_foi()
    declaration_page.agree_to_declaration(driver)
    functions.click_submit(driver)


@given(parsers.parse('I create "{decision}" final advice'))  # noqa
def final_advice(context, decision, api_test_client):  # noqa
    api_test_client.cases.create_final_advice(
        context.case_id, [{"type": decision, "text": "abc", "note": "", "good": context.goods[0]["good"]["id"]}]
    )


@given("I remove the flags")  # noqa
def i_remove_all_flags(context, api_test_client):  # noqa
    api_test_client.flags.assign_case_flags(context.case_id, [])


@given(parsers.parse('I create a licence for my application with "{decision}" decision document'))  # noqa
def create_licence(context, decision, api_test_client):  # noqa
    document_template = api_test_client.document_templates.add_template(
        api_test_client.picklists, case_types=["oiel", "siel", "exhc"]
    )

    api_test_client.cases.finalise_case(context.case_id, "approve")

    api_test_client.cases.add_generated_document(context.case_id, document_template["id"], decision)
    context.generated_document = api_test_client.context["generated_document"]

    if decision != "no_licence_required":
        api_test_client.cases.finalise_licence(context.case_id)
        context.licence = api_test_client.context["licence"]


@given(parsers.parse('I create a licence for my open application with "{decision}" decision document'))  # noqa
def create_open_licence(context, decision, api_test_client):  # noqa
    document_template = api_test_client.document_templates.add_template(api_test_client.picklists, case_types=["oiel"])

    api_test_client.cases.add_good_country_decisions(
        context.case_id, {f"{context.goods_type['id']}.{context.country['code']}": "approve"}
    )
    api_test_client.cases.finalise_case(context.case_id, "approve")

    api_test_client.cases.add_generated_document(context.case_id, document_template["id"], decision)
    context.generated_document = api_test_client.context["generated_document"]

    if decision != "no_licence_required":
        api_test_client.cases.finalise_licence(context.case_id)
        context.licence = api_test_client.context["licence"]


@given("I finalise my NLR decision")  # noqa
def finalise_case_with_nlr_decision(context, api_test_client):  # noqa
    document_template = api_test_client.document_templates.add_template(
        api_test_client.picklists, case_types=["oiel", "siel", "exhc"]
    )
    api_test_client.cases.finalise_case(context.case_id, "no_licence_required")
    api_test_client.cases.add_generated_document(context.case_id, document_template["id"], "no_licence_required")
    context.generated_document = api_test_client.context["generated_document"]
    api_test_client.cases.finalise_licence(context.case_id, save_licence=False)


@given(
    parsers.parse('I create a licence for my application with "{decision}" decision document and good decisions')
)  # noqa
def create_licence_with_licenced_goods(context, decision, api_test_client):  # noqa
    document_template = api_test_client.document_templates.add_template(
        api_test_client.picklists, case_types=["oiel", "siel", "exhc"]
    )
    additional_data = {}
    for good in context.goods:
        additional_data[f"quantity-{good['id']}"] = good["quantity"]
        additional_data[f"value-{good['id']}"] = round(float(good["value"]) * good["quantity"], 2)
    api_test_client.cases.finalise_case(context.case_id, "approve", additional_data)
    api_test_client.cases.add_generated_document(context.case_id, document_template["id"], decision)
    api_test_client.cases.finalise_licence(context.case_id)
    context.licence = api_test_client.context["licence"]


@then(parsers.parse('I can see the sections "{sections}" are on the task list'))  # noqa
def sections_appear_on_task_list(driver, sections):  # noqa
    sections = sections.split(", ")
    for section in sections:
        assert TaskListPage(driver).get_section(section) is not None


@given(parsers.parse('the status is set to "{status}"'))  # noqa
def set_status(api_test_client, context, status):  # noqa
    api_test_client.applications.set_status(context.app_id, status)


@then("I see my edited reference number")
def assert_ref_num(driver):  # noqa
    assert "12345678" in driver.find_element_by_css_selector(".lite-task-list").text


@when("I change my reference number")
def change_ref_num(driver, context):  # noqa
    enter_export_licence(driver, "yes", "12345678", context)


@when("I go to the licences page")
def licences_page(driver, exporter_url):  # noqa
    driver.get(exporter_url.rstrip("/") + "/licences/")


@given(parsers.parse('I create "{decision}" final advice for open application'))  # noqa
def final_advice_open(context, decision, api_test_client):  # noqa
    api_test_client.cases.create_final_advice(
        context.case_id,
        [
            {"type": decision, "text": "abc", "note": "", "goods_type": context.goods_type["id"]},
            {"type": decision, "text": "abc", "note": "", "country": context.country["code"]},
        ],
    )
