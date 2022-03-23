import os

from django.utils import timezone
from faker import Faker  # noqa
from pytest_bdd import given, when, then, parsers

import tests_common.tools.helpers as utils
from ui_tests.exporter.fixtures.add_end_user_advisory import add_end_user_advisory  # noqa
from ui_tests.exporter.fixtures.add_goods_query import add_goods_clc_query  # noqa
from ui_tests.exporter.fixtures.add_party import add_end_user_to_application  # noqa
from ui_tests.exporter.fixtures.env import environment  # noqa
from ui_tests.exporter.fixtures.manage_case import manage_case_status_to_withdrawn, approve_case  # noqa
from ui_tests.exporter.fixtures.register_organisation import (  # noqa
    register_organisation,
    register_organisation_for_switching_organisation,
)
from ui_tests.exporter.fixtures.sso_sign_in import sso_sign_in  # noqa
from ui_tests.exporter.pages.add_goods_page import AddGoodPage
from ui_tests.exporter.pages.add_goods_details import AddGoodDetails
from ui_tests.exporter.pages.add_end_user_pages import AddEndUserPages
from ui_tests.exporter.pages.application_edit_type_page import ApplicationEditTypePage
from ui_tests.exporter.pages.application_page import ApplicationPage
from ui_tests.exporter.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_tests.exporter.pages.attach_document_page import AttachDocumentPage
from ui_tests.exporter.pages.end_use_details_form_page import EndUseDetailsFormPage
from ui_tests.exporter.pages.exporter_hub_page import ExporterHubPage
from ui_tests.exporter.pages.generic_application.additional_documents import AdditionalDocumentsPage
from ui_tests.exporter.pages.generic_application.declaration import DeclarationPage
from ui_tests.exporter.pages.generic_application.task_list import TaskListPage
from ui_tests.exporter.pages.hub_page import Hub
from ui_tests.exporter.pages.mod_clearances.ExhibitionClearanceDetails import ExhibitionClearanceDetailsPage
from ui_tests.exporter.pages.open_application.add_goods_type import OpenApplicationAddGoodsType
from ui_tests.exporter.pages.product_summary import ProductSummary
from ui_tests.exporter.pages.respond_to_ecju_query_page import RespondToEcjuQueryPage
from ui_tests.exporter.pages.route_of_goods_form_page import RouteOfGoodsFormPage
from ui_tests.exporter.pages.shared import Shared
from ui_tests.exporter.pages.sites_page import SitesPage
from ui_tests.exporter.pages.standard_application.good_details import StandardApplicationGoodDetails
from ui_tests.exporter.pages.standard_application.goods import StandardApplicationGoodsPage
from ui_tests.exporter.pages.submitted_applications_page import SubmittedApplicationsPages
from ui_tests.exporter.pages.temporary_export_details_form_page import TemporaryExportDetailsFormPage
from ui_tests.exporter.pages.which_location_form_page import WhichLocationFormPage
from tests_common import functions
from tests_common.fixtures.add_a_document_template import (  # noqa
    add_a_document_template,
    get_paragraph_text,
    get_template_id,
    get_licence_template_id,
)
from tests_common.fixtures.add_a_draft import add_a_draft  # noqa
from tests_common.fixtures.add_a_generated_document import add_a_generated_document  # noqa
from tests_common.fixtures.apply_for_application import (  # noqa
    apply_for_standard_application,
    add_an_ecju_query,
    apply_for_open_application,
    apply_for_exhibition_clearance,
    apply_for_f680_clearance,
    apply_for_gifting_clearance,
    apply_for_standard_trade_control_application,
    apply_for_ogel,
)
from tests_common.fixtures.core import (  # noqa
    context,
    exporter_info,
    internal_info,
    api_client,
    api_test_client,
)
from tests_common.fixtures.driver import driver  # noqa
from tests_common.fixtures.urls import exporter_url, api_url  # noqa
from tests_common.tools.wait import wait_for_download_button_on_exporter_main_content

from ui_tests.exporter.pages.start_page import StartPage
from ui_tests.exporter.pages.great_signin_page import GreatSigninPage
from tests_common.helpers import applications


strict_gherkin = False
fake = Faker()


@given("I create a standard application via api")  # noqa
def standard_application_exists(apply_for_standard_application):  # noqa
    pass


@given("I create an open application via api")  # noqa
def open_application_exists(apply_for_open_application):  # noqa
    pass


@when("I go to application previously created")  # noqa
def click_on_an_application(driver, exporter_url, context):  # noqa
    driver.get(exporter_url.rstrip("/") + "/applications/" + context.app_id + "/task-list/")


@when("I click on the application just created")  # noqa
def click_on_application_just_created(driver, context):  # noqa
    driver.find_element_by_link_text(context.app_name).click()


@when("I click edit application")  # noqa
def i_click_edit_application(driver):  # noqa
    ApplicationPage(driver).click_edit_application_link()


@given("I signin and go to exporter homepage and choose Test Org")  # noqa
def go_to_exporter(driver, register_organisation, sso_sign_in, exporter_url, context, exporter_info):  # noqa
    driver.get(exporter_url)
    StartPage(driver).try_click_sign_in_button()

    if "login" in driver.current_url:
        GreatSigninPage(driver).sign_in(exporter_info["email"], exporter_info["password"])

    if "pick-organisation" in driver.current_url:
        no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), context.org_name)
        Shared(driver).click_on_radio_buttons(no)
        functions.click_submit(driver)
    elif Shared(driver).get_text_of_organisation_heading() != context.org_name:
        Hub(driver).click_switch_link()
        no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), context.org_name)
        Shared(driver).click_on_radio_buttons(no)
        functions.click_submit(driver)


@given("Only my email is to be processed by LITE-HMRC")
def only_my_email_is_to_be_processed_by_lite_hmrc(api_client):  # noqa

    # Mark all existing emails to be processed/sent so we can focus
    # on a single one
    url = f"/licences/hmrc-integration/mark-emails-as-processed/"
    response = api_client.make_request(method="GET", url=url, headers=api_client.exporter_headers)
    assert response.status_code == 200


@then("I logout")  # noqa
def i_logout(driver, exporter_url):  # noqa
    driver.get(exporter_url.rstrip("/") + "/auth/logout")
    if "accounts/logout" in driver.current_url:
        driver.find_element_by_css_selector("[action='/sso/accounts/logout/'] button").click()
        driver.get(exporter_url)


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


@when(parsers.parse('I click on the "{section_name}" section'))  # noqa
def go_to_task_list_section(driver, section_name):  # noqa
    section = driver.find_element_by_link_text(section_name)
    section_id = section.get_attribute("id")
    TaskListPage(driver).click_on_task_list_section(section_id)


@then(parsers.parse('the section "{section_name}" is now saved'))  # noqa
def verify_section_is_saved(driver, section_name):  # noqa
    section = driver.find_element_by_link_text(section_name)
    section_id = section.get_attribute("id")
    saved_status_element = driver.find_element_by_id(f"{section_id}-status")
    assert saved_status_element.text == "SAVED"


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


@when(parsers.parse('I answer "{choice}" for shipping air waybill or lading and Save'))  # noqa
def route_of_goods(driver, choice):  # noqa
    route_of_goods = RouteOfGoodsFormPage(driver)
    if choice == "No":
        route_of_goods.answer_route_of_goods_question(True, "Not shipped air waybill.")
    else:
        route_of_goods.answer_route_of_goods_question(False)

    functions.click_submit(driver)


@when(parsers.parse("I save and continue on the summary page"))  # noqa
def save_continue_summary_list(driver):  # noqa
    element = driver.find_element_by_css_selector("button[value='finish']")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    driver.execute_script("arguments[0].click();", element)


@when("I provide details of why my export is temporary")  # noqa
def enter_temporary_export_details(driver):  # noqa
    temporary_export_details = TemporaryExportDetailsFormPage(driver)
    temporary_export_details.answer_temp_export_details("Lorem ipsum")
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


@when(parsers.parse('I select "{choice}" and click submit'))
@when(parsers.parse('I select "{choice}" for where my goods will begin their export journey'))
@when(parsers.parse('I select "{choice}" when asked if the products are being permanently exported'))
@when(parsers.parse('I select "{choice}" when asked who the products are going to'))
def choose_who_products_going_to(driver, choice):  # noqa
    driver.find_element_by_xpath(f"//label/span[contains(text(), '{choice}')]").click()
    functions.click_submit(driver)


@when(parsers.parse('I select the site at position "{no}"'))  # noqa
def select_the_site_at_position(driver, no):  # noqa
    sites = SitesPage(driver)
    sites.click_sites_checkbox(int(no) - 1)


@when("I click on applications")  # noqa
def click_my_application_link(driver):  # noqa
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_applications()


@when("I click on draft tab for applications")  # noqa
def click_draft_tab(driver):  # noqa
    applications_page = ApplicationPage(driver)
    applications_page.click_draft_applications_tab()


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
    context.time_date_submitted = timezone.localtime().strftime("%I:%M%p").lstrip("0").replace(
        " 0", " "
    ).lower() + timezone.localtime().strftime(" %d %B %Y")


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


@when("I click to respond to the ECJU query")  # noqa
def respond_to_ecju_click(driver):  # noqa
    application_page = ApplicationPage(driver)
    application_page.respond_to_ecju_query(0)


@when(parsers.parse('I enter my response as "{response}"'))  # noqa
def enter_query_response(driver, response):  # noqa
    response_page = RespondToEcjuQueryPage(driver)
    response_page.enter_form_response(response)


@when(parsers.parse('I click "{button_value}"'))  # noqa
def click_button(driver, button_value):  # noqa
    functions.click_submit(driver, button_value=button_value)


@when(parsers.parse('I enter "{response}" for the response and click submit'))  # noqa
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


@when("I confirm I can upload a document")
def confirm_can_upload_document(driver):  # noqa
    # Confirm you have a document that is not sensitive
    AddGoodPage(driver).confirm_can_upload_good_document()
    functions.click_submit(driver)


@when(parsers.parse('I upload file "{filename}" with description "{description}"'))  # noqa
def upload_a_file_with_description(driver, filename, description):  # noqa
    attach_document_page = AttachDocumentPage(driver)
    file_path = get_file_upload_path(filename)
    attach_document_page.choose_file(file_path)
    attach_document_page.enter_description(description)
    functions.click_submit(driver)


@when(parsers.parse('I see the missing document reason text "{reason}"'))
def get_missing_document_reason(driver, reason):  # noqa
    response_page = RespondToEcjuQueryPage(driver)
    assert response_page.get_missing_document_reason_text() == reason


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


@when("I add an existing good to the application")  # noqa
def i_add_an_existing_good_to_the_application(driver, context):  # noqa
    goods_page = StandardApplicationGoodsPage(driver)
    goods_page.click_add_preexisting_good_button()

    # Click the "Add to application" link on the first good
    driver.find_elements_by_id("add-to-application")[0].click()


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
    if "ui_tests" not in file_to_upload_abs_path:
        file_to_upload_abs_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, "ui_tests/resources", filename)
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


@given("I remove the flags to finalise the licence")  # noqa
def i_remove_all_flags(context, api_test_client):  # noqa
    api_test_client.flags.assign_case_flags(context.case_id, [])
    api_test_client.gov_users.put_test_user_in_team("Licensing Unit")
    api_test_client.flags.assign_destination_flags(context.third_party["id"], [])
    api_test_client.gov_users.put_test_user_in_team("Admin")


@given("I put the test user in the admin team")
def put_test_user_in_admin_team(api_test_client):  # noqa
    api_test_client.gov_users.put_test_user_in_team("Admin")


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


@when(parsers.parse('I select product category "{product_category}"'))  # noqa
def select_product_category(driver, product_category):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.select_product_category(product_category)
    functions.click_submit(driver)


@when(parsers.parse('I select product type "{product_type}"'))  # noqa
def select_product_type(driver, product_type):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.select_firearm_product_type(product_type)
    functions.click_submit(driver)


@when(
    parsers.parse(
        'I select "{has_markings}" for serial number or other identification markings with details as "{details}"'
    )
)  # noqa
def specify_serial_number_of_other_identification_details(driver, has_markings, details):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.set_identification_details(has_markings, details)
    functions.click_submit(driver)


@when(parsers.parse('I specify number of items as "{number_of_items}"'))
def specify_number_of_items(driver, number_of_items):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.enter_number_of_items(number_of_items)
    functions.click_submit(driver)


@when(parsers.parse('I enter "{number_of_items}" serial numbers as "{serial_numbers}"'))
def enter_serial_numbers(driver, number_of_items, serial_numbers):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.enter_serial_numbers(int(number_of_items), serial_numbers.split(","))
    functions.click_submit(driver)


@when(
    parsers.parse(
        'I enter good name as "{name}" description as "{description}" part number "{part_number}" '
        'controlled "{controlled}" control code "{control_code}" and graded "{graded}"'
    )
)  # noqa
def create_a_new_good_in_application(driver, name, description, part_number, controlled, control_code, graded):  # noqa
    add_goods_page = AddGoodPage(driver)
    add_goods_page.enter_good_name(name)
    add_goods_page.enter_description_of_goods(description)
    add_goods_page.enter_part_number(part_number)
    add_goods_page.select_is_your_good_controlled(controlled)
    add_goods_page.enter_control_list_entries(control_code)
    add_goods_page.select_is_your_good_graded(graded)
    functions.click_submit(driver)


@when(parsers.parse('I enter firearm year of manufacture as "{year}"'))
def enter_firearm_year_of_manufacture(driver, year):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.enter_year_of_manufacture(year)
    functions.click_submit(driver)


@when(parsers.parse('I select firearm replica status as "{status}" with description "{description}"'))
def enter_firearm_replica_status_with_description(driver, status, description):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.select_replica_status(status, description)
    functions.click_submit(driver)


@when(parsers.parse('I enter calibre as "{calibre}"'))
def enter_firearm_calibre(driver, calibre):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.enter_calibre(calibre)
    functions.click_submit(driver)


@when(parsers.parse('I specify firearms act sections apply as "{choice}"'))
def specify_firearms_act_sections_choice(driver, choice):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.select_do_firearms_act_sections_apply(choice)

    if choice != "Yes":
        functions.click_submit(driver)


@when(parsers.parse('I select firearms act section "{num}"'))
def specify_firearms_act_section_num(driver, num):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.select_firearms_act_section(num)
    functions.click_submit(driver)


@when(parsers.parse('I upload firearms certificate file "{filename}"'))  # noqa
def upload_a_file_with_description(driver, filename):  # noqa
    good_details_page = AddGoodDetails(driver)
    file_path = get_file_upload_path(filename)
    good_details_page.choose_firearms_certificate_file(file_path)


@when(parsers.parse('I enter certificate number as "{cert_num}" with expiry date "{expiry_date}"'))  # noqa
def upload_a_file_with_description(driver, cert_num, expiry_date):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.enter_firearms_act_certificate_number(cert_num)
    day, month, year = expiry_date.split("-")
    good_details_page.enter_certificate_expiry_date(day, month, year)
    functions.click_submit(driver)


@when(parsers.parse('I specify firearms identification markings as "{has_markings}" with details "{details}"'))
def specify_firearms_identification_markings(driver, has_markings, details):  # noqa
    good_details_page = AddGoodDetails(driver)
    good_details_page.does_firearm_have_identification_markings(has_markings, details)
    functions.click_submit(driver)


@when(parsers.parse('I specify military use details as "{military_use}"'))  # noqa
def specify_product_military_details(driver, military_use):  # noqa
    page = AddGoodDetails(driver)
    page.select_is_product_for_military_use(military_use)
    functions.click_submit(driver)


@when(parsers.parse('I specify component details as "{component}"'))  # noqa
def specify_product_component_details(driver, component):  # noqa
    page = AddGoodDetails(driver)
    page.select_is_product_a_component(component)
    functions.click_submit(driver)


@when(parsers.parse('I specify the "{product_type}" product purpose as "{purpose}"'))  # noqa
def specify_product_purpose_details(driver, product_type, purpose):  # noqa
    page = AddGoodDetails(driver)
    heading = driver.find_element_by_class_name("govuk-fieldset__heading").text
    assert f"Describe the purpose of the {product_type}" == heading
    page.enter_software_technology_purpose_details(purpose)
    functions.click_submit(driver)


@when(parsers.parse('I specify product employs information security features as "{supports_infosec}"'))  # noqa
def specify_product_infosec_details(driver, supports_infosec):  # noqa
    page = AddGoodDetails(driver)
    page.does_product_employ_information_security(supports_infosec)
    functions.click_submit(driver)


@when(parsers.parse('I see summary screen for "{product_type_value}" product with name "{name}" and "{proceed}"'))
def summary_screen_for_product_type(driver, product_type_value, name, proceed):  # noqa
    summary_page = ProductSummary(driver)
    assert summary_page.get_page_heading() == "Product summary"
    summary = summary_page.get_summary_details()
    assert summary["Product type"] == product_type_value
    assert summary["Name"] == name
    expected_fields = [
        "Part number",
        "CLC",
        "Security grading",
    ]

    if product_type_value == "Firearms":
        expected_fields += [
            "Year of manufacture",
            "Replica firearm",
            "Calibre",
            "Identification markings",
        ]
    elif product_type_value == "Accessory of a firearm":
        expected_fields += [
            "Military use",
            "Component",
            "Information security features",
        ]

    assert all(key in summary.keys() for key in expected_fields)

    if proceed == "continue":
        driver.find_element_by_link_text("Continue").click()


@when(parsers.parse('I enter product details with value "{value}" and deactivated "{status}" and Save'))  # noqa
def i_enter_product_details_and_value(driver, value, status):  # noqa
    details_page = StandardApplicationGoodDetails(driver)
    details_page.enter_value(value)
    details_page.check_is_good_incorporated_false()
    # this step is not applicable if we are adding an existing good to the application
    if status != "N/A":
        details_page.set_deactivated_status(status)

    functions.click_submit(driver)


@when(
    parsers.parse(
        'I enter product details with unit of measurement "{unit}", quantity "{quantity}", value "{value}" and deactivated "{status}" and Save'
    )
)  # noqa
def i_enter_product_details_unit_quantity_and_value(driver, unit, quantity, value, status):  # noqa
    details_page = StandardApplicationGoodDetails(driver)
    details_page.select_unit(unit)
    details_page.enter_quantity(quantity)
    details_page.enter_value(value)
    details_page.check_is_good_incorporated_false()
    # this step is not applicable if we are adding an existing good to the application
    if status != "N/A":
        details_page.set_deactivated_status(status)

    functions.click_submit(driver)


@then(parsers.parse('the product with name "{expected}" is added to the application'))
def product_with_name_is_added_to_application(driver, expected):  # noqa
    products_page = StandardApplicationGoodsPage(driver)
    actual = products_page.get_product_name()
    assert actual == expected


@then(parsers.parse('the product "{description}" is added to the application'))
def product_with_description_is_added_to_application(driver, description):  # noqa
    products_page = StandardApplicationGoodsPage(driver)
    assert products_page.good_with_description_exists(description)


@when(parsers.parse('I can edit good "{field_name}" as "{updated_value}"'))  # noqa
def edit_good_details_in_application(driver, field_name, updated_value):  # noqa
    summary_page = ProductSummary(driver)
    _, link = summary_page.get_field_details(field_name)
    driver.execute_script("arguments[0].scrollIntoView();", link)
    driver.execute_script("arguments[0].click();", link)

    pages_map = {
        "Name": AddGoodPage(driver).enter_good_name,
        "Description": AddGoodPage(driver).enter_description_of_goods,
        "Part number": AddGoodPage(driver).enter_part_number,
        "Year of manufacture": AddGoodDetails(driver).enter_year_of_manufacture,
        "Calibre": AddGoodDetails(driver).enter_calibre,
        "Military use": AddGoodDetails(driver).select_is_product_for_military_use,
        "Information security features": AddGoodDetails(driver).does_product_employ_information_security,
    }

    func = pages_map[field_name]
    assert func is not None
    func(updated_value)
    functions.click_submit(driver)

    if field_name == "Military use":
        if updated_value == "yes_designed":
            updated_value = "Yes, specially designed for military use"
        elif updated_value == "yes_modified":
            updated_value = "Yes, modified for military use"
        elif updated_value == "no":
            updated_value = "No"

    updated_field_value, _ = summary_page.get_field_details(field_name)
    assert updated_field_value == updated_value


@when(parsers.parse('I click on "{link_text}"'))  # noqa
def click_link_with_text(driver, link_text):  # noqa
    driver.find_element_by_link_text(link_text).click()


@then("I see the temporary export detail summary")  # noqa
def i_see_temporary_export_detail_summary(driver):  # noqa
    heading = driver.find_element_by_tag_name("h1").text
    assert heading == "Temporary export details summary list"
    elements = driver.find_elements_by_tag_name("dd")
    assert elements[0].text == "Lorem ipsum"
    assert elements[2].text == "Yes"
    assert elements[4].text == "2030-01-01"
    functions.click_finish_button(driver)


@when(parsers.parse('I answer "{option}" for whether I want to reuse an existing party'))  # noqa
def reuse_existing_party(driver, option):  # noqa
    add_end_user_page = AddEndUserPages(driver)
    add_end_user_page.choose_reuse_existing_party(option)
    functions.click_submit(driver)


@when(parsers.parse('I select "{consignee_type}" as the type of consignee'))  # noqa
def select_consignee_type(driver, consignee_type):  # noqa
    consignee_page = AddEndUserPages(driver)
    consignee_page.select_type(consignee_type)
    functions.click_submit(driver)


@when(parsers.parse('I select a party with type of "{consignee_type}"'))  # noqa
def select_party(driver, consignee_type):  # noqa
    party_rows = driver.find_elements_by_xpath("//tr[@class='govuk-table__row']")
    for party_row in party_rows:
        if consignee_type.lower() in party_row.text.lower():
            party_row.find_element_by_class_name("lite-button--link").click()
            return


@when(parsers.parse('I select "{end_user_type}" as the type of end user'))  # noqa
def select_end_user_type(driver, end_user_type):  # noqa
    add_end_user_page = AddEndUserPages(driver)
    add_end_user_page.select_type(end_user_type)
    functions.click_submit(driver)


@when(parsers.parse('I enter the "{consignee_name}" as the consignee name'))  # noqa
def enter_consignee_name(driver, consignee_name):  # noqa
    consignee_page = AddEndUserPages(driver)
    consignee_page.enter_name(consignee_name)
    functions.click_submit(driver)


@when(parsers.parse('I enter the "{end_user_name}" as end user name'))  # noqa
def enter_end_user_name(driver, end_user_name):  # noqa
    add_end_user_page = AddEndUserPages(driver)
    add_end_user_page.enter_name(end_user_name)
    functions.click_submit(driver)


@when(parsers.parse('I enter "{address}" and "{country}" for end user address'))  # noqa
def enter_end_user_address(driver, address, country):  # noqa
    add_end_user_page = AddEndUserPages(driver)
    add_end_user_page.enter_address(address)
    add_end_user_page.enter_country(country)
    functions.click_submit(driver)


@when(parsers.parse('I enter "{address}" and "{country}" for consignee address'))  # noqa
def enter_consignee_address(driver, address, country):  # noqa
    add_consignee_page = AddEndUserPages(driver)
    add_consignee_page.enter_address(address)
    add_consignee_page.enter_country(country)
    functions.click_submit(driver)


@when(parsers.parse('I enter "{sig_name}" for signatory name'))  # noqa
def enter_sig_name(driver, sig_name):  # noqa
    add_end_user_page = AddEndUserPages(driver)
    add_end_user_page.enter_signatory_name(sig_name)
    functions.click_submit(driver)


@then("I see the end user summary")  # noqa
def i_see_end_user_summary(driver):  # noqa
    heading = driver.find_element_by_tag_name("h1").text
    assert heading == "End user"
    elements = driver.find_elements_by_tag_name("dd")
    assert elements[0].text == "Foo Bar"
    assert elements[1].text == "Government"
    assert elements[2].text == "Test Address, Belgium"
    assert elements[3].text == "N/A"
    assert elements[4].text == "Test signatory"


@then("I see the consignee summary")  # noqa
def i_see_consignee_summary(driver):  # noqa
    heading = driver.find_element_by_tag_name("h1").text
    assert heading == "Consignee"
    elements = driver.find_elements_by_tag_name("dd")
    assert elements[0].text == "Foo Bar"
    assert elements[1].text == "Government"
    assert elements[2].text == "Test Address, Belgium"
    assert elements[3].text == "N/A"


@then("I see Government in the consignee summary")  # noqa
def i_see_consignee_summary(driver):  # noqa
    heading = driver.find_element_by_tag_name("h1").text
    assert heading == "Consignee"
    elements = driver.find_elements_by_tag_name("dd")
    assert elements[1].text == "Government"


@given(
    "I create an application with <name>,<product>,<part_number>,<clc_rating>,<end_user_name>,<end_user_address>,"
    "<consignee_name>,<consignee_address>,<country>,<end_use>",
    target_fixture="create_application",
)
def create_application(
    api_test_client,  # noqa
    context,  # noqa
    name,
    product,
    part_number,
    clc_rating,
    end_user_name,
    end_user_address,
    consignee_name,
    consignee_address,
    country,
    end_use,
):
    app_data = {
        "name": name,
        "product": product,
        "part_number": part_number,
        "clc_rating": clc_rating,
        "end_user_name": end_user_name,
        "end_user_address": end_user_address,
        "consignee_name": consignee_name,
        "consignee_address": consignee_address,
        "country": country,
        "end_use": end_use,
    }
    applications.create_standard_application(api_test_client, context, app_data, submit=False)


@given(
    "I submit an application with <name>,<product>,<clc_rating>,<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>",
    target_fixture="submit_application",
)
def submit_application(
    api_test_client,  # noqa
    context,  # noqa
    name,
    product,
    clc_rating,
    end_user_name,
    end_user_address,
    consignee_name,
    consignee_address,
    country,
    end_use,
):
    app_data = {
        "name": name,
        "product": product,
        "clc_rating": clc_rating,
        "end_user_name": end_user_name,
        "end_user_address": end_user_address,
        "consignee_name": consignee_name,
        "consignee_address": consignee_address,
        "country": country,
        "end_use": end_use,
    }
    applications.create_standard_application(api_test_client, context, app_data, submit=True)


@given("I create an ecju query")
def create_ecju_query(api_test_client, context):  # noqa
    api_test_client.ecju_queries.add_ecju_query(context.case_id)


@given("I navigate to application summary")
def navigate_to_application(driver, exporter_url, context):  # noqa
    driver.get(f"{exporter_url}applications/{context.app_id}/task-list")
    functions.click_submit(driver)


@then("I see the application summary with <clc_rating>,<end_use>,<end_user_name>,<consignee_name>,<part_number>")
def i_see_application_summary(driver, clc_rating, end_use, end_user_name, consignee_name, part_number):  # noqa
    tds = driver.find_elements_by_tag_name("td")
    dds = driver.find_elements_by_tag_name("dd")
    assert tds[2].text == part_number
    assert tds[4].text == clc_rating
    assert tds[10].text == end_use
    assert dds[6].text == end_user_name
    assert dds[12].text == consignee_name
    functions.click_submit(driver)


@when("I agree to the declaration")
def i_agree(driver):  # noqa
    driver.find_element_by_id("agreed_to_declaration_text").send_keys("I AGREE")
    functions.click_submit(driver)


@then("the application is submitted")
def application_submitted(driver, context):  # noqa
    assert driver.find_element_by_tag_name("h1").text == "Application submitted"


@when("I click on my application")
def click_on_application(driver, context):  # noqa
    elements = Shared(driver).get_gov_table_cell_links()
    no = utils.get_element_index_by_text(elements, context.app_name, complete_match=False)
    elements[no].click()
