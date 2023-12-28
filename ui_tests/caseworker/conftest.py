import json

from django.utils import timezone
from pytest_bdd import given, when, then, parsers
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from core.constants import CaseStatusEnum
from ui_tests.caseworker.pages.advice import FinalAdvicePage, TeamAdvicePage
from ui_tests.caseworker.pages.case_page import CasePage, CaseTabs
from ui_tests.caseworker.pages.teams_pages import TeamsPages
from ui_tests.caseworker.pages.case_officer_page import CaseOfficerPage
from caseworker.core.constants import DATE_FORMAT
from ui_tests.caseworker.fixtures.env import environment  # noqa
from ui_tests.caseworker.fixtures.add_a_flag import (  # noqa
    add_case_flag,
    add_good_flag,
    add_organisation_flag,
    add_destination_flag,
    get_flag_of_level,
)
from ui_tests.caseworker.fixtures.add_queue import add_queue  # noqa
from ui_tests.caseworker.fixtures.add_a_document_template import (  # noqa
    add_a_document_template,
    get_template_id,
)
from ui_tests.caseworker.fixtures.add_a_picklist import (  # noqa
    add_a_letter_paragraph_picklist,
    add_an_ecju_query_picklist,
    add_a_proviso_picklist,
    add_a_standard_advice_picklist,
    add_a_report_summary_picklist,
)
from ui_tests.caseworker.pages.generate_decision_documents_page import GeneratedDecisionDocuments
from ui_tests.caseworker.pages.generate_document_page import GeneratedDocument
from ui_tests.caseworker.pages.give_advice_pages import GiveAdvicePages
from ui_tests.caseworker.pages.good_country_matrix_page import GoodCountryMatrixPage
from ui_tests.caseworker.pages.grant_licence_page import GrantLicencePage
from ui_tests.caseworker.pages.letter_templates import LetterTemplates
from ui_tests.caseworker.pages.shared import Shared
from tests_common import functions
from tests_common.fixtures.driver import driver  # noqa
from tests_common.fixtures.apply_for_application import *  # noqa
from tests_common.fixtures.sso_sign_in import sso_sign_in  # noqa
from tests_common.fixtures.core import (  # noqa
    context,  # noqa
    api_test_client,
    exporter_info,  # noqa
    internal_info,  # noqa
    api_client,  # noqa
)  # noqa
from tests_common.fixtures.urls import internal_url, sso_sign_in_url, api_url  # noqa

import tests_common.tools.helpers as utils
from ui_tests.caseworker.pages.case_list_page import CaseListPage
from ui_tests.caseworker.pages.application_page import ApplicationPage
from tests_common.helpers import applications
from ui_tests.exporter.pages.add_goods_page import AddGoodPage
from ui_tests.caseworker.pages.product_assessment import ProductAssessmentPage


@when("I go to the internal homepage")  # noqa
def when_go_to_internal_homepage(driver, internal_url):  # noqa
    driver.get(internal_url)


@given("I go to internal homepage")  # noqa
def go_to_internal_homepage(driver, internal_url):  # noqa
    driver.get(internal_url)


@given("I sign in to SSO or am signed into SSO")  # noqa
def sign_into_sso(driver, sso_sign_in):  # noqa
    pass


@then("I go to application previously created")  # noqa
@when("I go to application previously created")  # noqa
def click_on_created_application(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.case_id + "/")
    driver.find_element(by=By.ID, value="tab-details").click()


@given("I create standard application or standard application has been previously created")  # noqa
def create_app(driver, apply_for_standard_application):  # noqa
    pass


@given(
    "I create an application with <name>,<product>,<part_number>,<clc_rating>,"
    "<end_user_name>,<end_user_address>,<consignee_name>,<consignee_address>,<country>,<end_use>",
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
    applications.create_standard_application(api_test_client, context, app_data)


@then(parsers.parse('I should see the product name as "{product_name}" with product rating as "{clc_rating}"'))
def check_product_name_and_rating(driver, product_name, clc_rating):  # noqa
    product_table = driver.find_element(by=By.ID, value="table-goods")
    name_element = product_table.find_element(by=By.XPATH, value="//tbody/tr/td[3]")
    rating_element = product_table.find_element(by=By.XPATH, value="//tbody/tr/td[6]")
    assert name_element.text == product_name
    assert rating_element.text == clc_rating


@then(parsers.parse('I check the product part number is "{part_number}"'))
def check_product_part_number(driver, part_number):  # noqa
    product_table = driver.find_element(by=By.CLASS_NAME, value="govuk-table")
    pn_element = product_table.find_element(by=By.XPATH, value="//tbody/tr[4]/td")
    assert pn_element.text == part_number


@then(parsers.parse('I check the product annual report summary is "{report_summary}"'))
def check_product_report_summary(driver, report_summary):  # noqa
    product_table = driver.find_element(by=By.ID, value="table-goods")
    summary_element = product_table.find_element(by=By.XPATH, value="//tbody/tr/td[9]")
    assert summary_element.text == report_summary


@then(parsers.parse('I should see "{timeline_text}" appear in the timeline'))
def check_timeline(driver, timeline_text):  # noqa
    assert timeline_text in Shared(driver).get_audit_trail_text_timeline()


@given("I create open application or open application has been previously created")  # noqa
def create_open_app(driver, apply_for_open_application):  # noqa
    pass


@given("I prepare the application for final review NLR")
def prepare_for_final_review_nlr(api_test_client):  # noqa
    prepare_case(api_test_client, nlr=True)


@given("I prepare the application for final review")
def prepare_for_final_review(api_test_client):  # noqa
    prepare_case(api_test_client, nlr=False)


def prepare_case(api_test_client, nlr):  # noqa
    api_test_client.gov_users.put_test_user_in_team("Admin")
    api_test_client.flags.assign_case_flags(api_test_client.context["case_id"], [])
    api_test_client.gov_users.put_test_user_in_team("Licensing Unit")
    api_test_client.flags.assign_destination_flags(
        [
            api_test_client.context["end_user"]["id"],
            api_test_client.context["ultimate_end_user"]["id"],
            api_test_client.context["consignee"]["id"],
            api_test_client.context["third_party"]["id"],
        ],
        [],
    )
    api_test_client.goods.update_good_clc(
        good_id=api_test_client.context["good_id"],
        good_on_application_id=api_test_client.context["good_on_application_id"],
        case_id=api_test_client.context["case_id"],
        control_list_entries=["ML1a"] if not nlr else [],
        is_good_controlled=not nlr,
        report_summary="ARS",
    )
    api_test_client.cases.manage_case_status(
        api_test_client.context["case_id"], status=CaseStatusEnum.UNDER_FINAL_REVIEW
    )


@when("I click save and continue")
@when("I click save")
@when("I click send")
@when("I click preview")
@when("I click confirm")
@when("I click continue")
@when("I click submit")
def submit_form(driver):  # noqa
    old_page = driver.find_element(by=By.TAG_NAME, value="html")
    Shared(driver).click_submit()
    WebDriverWait(driver, 45).until(expected_conditions.staleness_of(old_page))


@when(parsers.parse('I click the text "{text}"'))
def click_text(driver, text):  # noqa
    xpath = f"//*[text()[contains(.,'{text}')]]"
    driver.find_element(by=By.XPATH, value=xpath).click()


@when(parsers.parse('I click "{button_text}"'))
def click_button_with_text(driver, button_text):  # noqa
    WebDriverWait(driver, 20).until(
        expected_conditions.presence_of_element_located(
            (
                By.XPATH,
                (
                    f"//button[contains(@class, 'govuk-button') and contains(text(), '{button_text}')] "
                    f"| //a[contains(@class, 'govuk-button') and contains(text(), '{button_text}')]"
                ),
            )
        )
    ).click()


@when("I click back")
def click_back_link(driver):  # noqa
    driver.find_element(by=By.LINK_TEXT, value="Back").click()


@when("I click change status")  # noqa
def click_post_note(driver):  # noqa
    case_page = CasePage(driver)
    case_page.change_tab(CaseTabs.DETAILS)
    case_page.click_change_status()


@when(parsers.parse('I select status "{status}" and save'))  # noqa
def select_status_save(driver, status, context):  # noqa
    application_page = ApplicationPage(driver)
    application_page.select_status(status)
    context.status = status
    context.date_time_of_update = utils.get_formatted_date_time_h_m_pm_d_m_y()
    Shared(driver).click_submit()


@when("I click on new queue in dropdown")  # noqa
@when("I click on edited queue in dropdown")  # noqa
def queue_shown_in_dropdown(driver, context):  # noqa
    CaseListPage(driver).click_on_queue_name(context.queue_name)


@when("I go to queues")  # noqa
def go_to_queues(driver, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/manage/")


@when("I add case to newly created queue")  # noqa
def move_case_to_new_queue(driver, context):  # noqa
    ApplicationPage(driver).click_move_case_button()
    if not driver.find_element(by=By.ID, value=context.queue_name.replace(" ", "-")).is_selected():
        driver.find_element(by=By.ID, value=context.queue_name.replace(" ", "-")).click()
    Shared(driver).click_submit()


@given("I create report summary picklist")  # noqa
def add_report_summary_picklist(add_a_report_summary_picklist):  # noqa
    pass


@then("I see previously created application")  # noqa
def should_see_previously_created_application(driver, context):  # noqa
    case_page = CaseListPage(driver)
    functions.open_case_filters(driver)
    case_page.click_clear_filters_button()
    case_page = CaseListPage(driver)
    functions.open_case_filters(driver)
    case_page.filter_by_case_reference(context.reference_code)
    functions.click_apply_filters(driver)
    assert driver.find_element(by=By.ID, value=context.case_id).is_displayed()


@when("I click on the application previously created")
def click_on_case(driver, context):  # noqa
    driver.find_element(by=By.ID, value=f"case-{context.case_id}").click()
    driver.find_element(by=By.ID, value=f"tab-details").click()


@when("I click on show filters")
def i_show_filters(driver):  # noqa
    functions.open_case_filters(driver)


@when(parsers.parse('I click on "{tab_name}" tab'))
def i_click_on_case_details_tab(driver, tab_name):  # noqa
    tabs = driver.find_element(by=By.CLASS_NAME, value="lite-tabs")
    target = tabs.find_element(by=By.LINK_TEXT, value=tab_name)
    target.click()


@when(parsers.parse('I filter by application type "{application_type}"'))
def filter_by_application_type(driver, application_type):  # noqa
    CaseListPage(driver).select_filter_case_type_from_dropdown(application_type)
    functions.click_apply_filters(driver)


@when("I go to users")  # noqa
def go_to_users(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/users/")


@when("I go to the case list page")  # noqa
def case_list_page(driver, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/")


@when("I go to my profile page")  # noqa
def get_profile_page(driver):  # noqa
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.ID, "link-profile"))).click()


@when(parsers.parse('I change my team to "{team}" and default queue to "{queue}"'))  # noqa
def go_to_team_edit_page(driver, team, queue):  # noqa
    # we should already be on the profile page
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.ID, "link-edit-team"))).click()
    teams_page = TeamsPages(driver)
    teams_page.select_team_from_dropdown(team)
    teams_page.select_default_queue_from_dropdown(queue)
    functions.click_submit(driver)
    # Ensure we return to the profile page
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.ID, "link-edit-team")))
    # Check that the team/queue change was applied successfully
    assert driver.find_element(by=By.ID, value="user-team-name").text == team
    assert driver.find_element(by=By.ID, value="user-default-queue").text == queue


@when("I go to my case list")  # noqa
def get_my_case_list(driver):  # noqa
    """
    Clicks on the menu and selects Cases
    Depending on team, default queue the list of cases will be different
    """
    driver.find_element(by=By.ID, value="link-menu").click()
    driver.find_element(by=By.LINK_TEXT, value="Cases").click()


@when("I click the application previously created")
def i_click_application_previously_created(driver, context):  # noqa
    case_list_page = CaseListPage(driver)
    functions.open_case_filters(driver)
    case_list_page.click_clear_filters_button()
    functions.open_case_filters(driver)
    case_list_page.filter_by_case_reference(context.reference_code)
    functions.click_apply_filters(driver)

    case_list_page.click_on_case(context.case_id)


@when(parsers.parse('I switch to queue "{queue}"'))  # noqa
def switch_queue_dropdown(driver, queue):  # noqa
    driver.find_element(by=By.ID, value="link-queue").click()
    queues = driver.find_element(by=By.ID, value="queues")
    queues.find_element(by=By.XPATH, value=f"//a[contains(text(), '{queue}')]").click()


@then("I should see my case in the cases list")  # noqa
def case_in_cases_list(driver, context):  # noqa
    case_page = CaseListPage(driver)
    functions.open_case_filters(driver)
    case_page.click_clear_filters_button()
    case_page = CaseListPage(driver)
    functions.open_case_filters(driver)
    case_page.filter_by_case_reference(context.reference_code)
    functions.click_apply_filters(driver)

    context.case_row = CaseListPage(driver).get_case_row(context.case_id)
    assert context.reference_code in context.case_row.text


@then("I should be able to customise the queue view")  # noqa
def customise_queue_view(driver, context):  # noqa
    case_in_cases_list(driver, context)

    case_row = CaseListPage(driver).get_case_row(context.case_id)
    assert f"{context.application_data['product']} (1234)" not in case_row.text
    assert "£10.24" not in case_row.text
    assert context.application_data["end_use"] not in case_row.text

    # Open customiser options
    customiser_options_selector = f"details.customiser__options summary"
    driver.find_element(by=By.CSS_SELECTOR, value=customiser_options_selector).click()

    # Click each checkbox to show the column
    columns_to_show = [
        "products",
        "control_list_entry",
        "report_summary",
        "regime",
        "total_value",
        "queries",
        "denial_matches",
        "intended_end_use",
    ]
    for column in columns_to_show:
        element_id = f"customiser__option-{column}"
        driver.find_element(by=By.ID, value=element_id).click()

    # Close the customiser options
    driver.find_element(by=By.CSS_SELECTOR, value=customiser_options_selector).click()

    case_row = CaseListPage(driver).get_case_row(context.case_id)

    # Ensure that expected extra values show up in case row
    assert f"{context.application_data['product']} (1234)" in case_row.text
    assert "£10.24" in case_row.text
    assert context.application_data["end_use"] in case_row.text

    # Clear localstorage so other tests start fresh
    driver.execute_script("return window.localStorage.clear();")


@then("I should see there are no new cases")
def no_new_cases(driver, context):  # noqa
    case_page = CaseListPage(driver)
    functions.open_case_filters(driver)
    case_page.click_clear_filters_button()
    case_page = CaseListPage(driver)
    functions.open_case_filters(driver)
    case_page.filter_by_case_reference(context.reference_code)
    functions.click_apply_filters(driver)
    assert "There are no new cases" in driver.find_element(by=By.ID, value="form-cases").text


@then("I should see my case SLA")  # noqa
def case_sla(driver, context):  # noqa
    assert CaseListPage(driver).get_case_row_sla(context.case_row) == "0"


@then("I see the case page")  # noqa
def i_see_the_case_page(driver, context):  # noqa
    assert context.reference_code in driver.find_element(by=By.ID, value=ApplicationPage.HEADING_ID).text


@then(parsers.parse('I see the case status is now "{status}"'))
def should_see_case_status(driver, status):  # noqa
    assert CasePage(driver).get_status() == status


@when("I go to users")  # noqa
def go_to_users(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/users/")


@given("an Exhibition Clearance is created")  # noqa
def an_exhibition_clearance_is_created(driver, apply_for_exhibition_clearance):  # noqa
    pass


@when("I combine all team advice")  # noqa
def combine_all_advice(driver):  # noqa
    TeamAdvicePage(driver).click_combine_advice()


@when("I finalise the advice")  # noqa
def finalise(driver):  # noqa
    CasePage(driver).change_tab(CaseTabs.FINAL_ADVICE)
    FinalAdvicePage(driver).click_finalise()


@when("I select the template previously created")  # noqa
def selected_created_template(driver, context):  # noqa
    GeneratedDocument(driver).click_letter_template(context.document_template_id)
    Shared(driver).click_submit()


@when(parsers.parse('I select the template "{template_name}"'))  # noqa
def select_template_by_name(driver, template_name):  # noqa
    GeneratedDocument(driver).select_document_template_by_name(template_name)


@when("I go to the documents tab")  # noqa
def click_documents(driver):  # noqa
    CasePage(driver).change_tab(CaseTabs.DOCUMENTS)


@when("I click I'm done")  # noqa
def im_done_button(driver):  # noqa
    ApplicationPage(driver).click_im_done_button()


@when("I go to my work queue")  # noqa
def work_queue(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/" + context.queue_id)


@then("my case is not in the queue")  # noqa
def my_case_not_in_queue(driver, context):  # noqa
    assert context.case_id not in Shared(driver).get_text_of_cases_form()


@given("a queue has been created")  # noqa
def create_queue(context, api_test_client):  # noqa
    api_test_client.queues.add_queue(f"queue {utils.get_formatted_date_time_y_m_d_h_s()}")
    context.queue_id = api_test_client.context["queue_id"]
    context.queue_name = api_test_client.context["queue_name"]


@given(parsers.parse('I "{decision}" all elements of the application at user and team level'))  # noqa
def approve_application_objects(context, api_test_client, decision):  # noqa
    context.advice_type = decision
    text = "abc"
    note = ""
    footnote_required = "False"
    data = [
        {
            "type": context.advice_type,
            "text": text,
            "note": note,
            "end_user": context.end_user["id"],
            "footnote_required": footnote_required,
        },
        {
            "type": context.advice_type,
            "text": text,
            "note": note,
            "consignee": context.consignee["id"],
            "footnote_required": footnote_required,
        },
        {
            "type": context.advice_type,
            "text": text,
            "note": note,
            "good": context.good_id,
            "footnote_required": footnote_required,
        },
    ]

    api_test_client.cases.create_user_advice(context.case_id, data)
    api_test_client.cases.create_team_advice(context.case_id, data)


@when("I click edit flags link")  # noqa
def click_edit_case_flags_link(driver):  # noqa
    CasePage(driver).click_change_case_flags()


@given(parsers.parse('the status is set to "{status}"'))  # noqa
def set_status(api_test_client, context, status):  # noqa
    api_test_client.applications.set_status(context.app_id, status)


@given("case has been moved to new Queue")  # noqa
def assign_case_to_queue(api_test_client):  # noqa
    api_test_client.cases.assign_case_to_queue()


@given("all flags are removed")  # noqa
def remove_all_flags(context, api_test_client):  # noqa
    api_test_client.flags.assign_case_flags(context.case_id, [])


@when("I add a new queue")  # noqa
def add_a_queue(driver, context, add_queue):  # noqa
    pass


@then("I see my autogenerated application form")  # noqa
def generated_document(driver, context):  # noqa
    latest_document = GeneratedDocument(driver).get_latest_document()

    assert "Application Form" in latest_document.text
    assert GeneratedDocument(driver).check_download_link_is_present(latest_document)


@then("the status has been changed in the application")  # noqa
def audit_trail_updated(driver, context, internal_info, internal_url):  # noqa
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)

    assert (
        context.status.lower() in Shared(driver).get_audit_trail_text().lower()
    ), "status has not been shown as approved in audit trail"


@given("I create a proviso picklist")  # noqa
def i_create_an_proviso_picklist(context, add_a_proviso_picklist):  # noqa
    context.proviso_picklist_name = add_a_proviso_picklist["name"]
    context.proviso_picklist_question_text = add_a_proviso_picklist["text"]


@given("I create a standard advice picklist")  # noqa
def i_create_an_standard_advice_picklist(context, add_a_standard_advice_picklist):  # noqa
    context.standard_advice_query_picklist_name = add_a_standard_advice_picklist["name"]
    context.standard_advice_query_picklist_question_text = add_a_standard_advice_picklist["text"]


@when(parsers.parse('I expand the details for "{details_text}"'))
def expand_details_for(driver, details_text):  # noqa
    driver.find_element(
        by=By.XPATH, value=f"//details[@class='govuk-details']/summary/span[contains(text(), '{details_text}')]"
    ).click()


@when(parsers.parse("I import text from the '{option}' picklist"))  # noqa
def import_text_advice(driver, option, context):  # noqa
    GiveAdvicePages(driver).click_on_import_link(option)
    text = GiveAdvicePages(driver).get_text_of_picklist_item()
    context.advice_data.append(text)
    GiveAdvicePages(driver).click_on_picklist_item(option)


@when(parsers.parse("I write '{text}' in the note text field"))  # noqa
def write_note_text_field(driver, text, context):  # noqa
    GiveAdvicePages(driver).type_in_additional_note_text_field(text)
    context.advice_data.append(text)


@when(parsers.parse("I select that a footnote is not required"))  # noqa
def write_note_text_field(driver, text, context):  # noqa
    GiveAdvicePages(driver).select_footnote_not_required()


@given("I create a letter paragraph picklist")  # noqa
def add_letter_paragraph_picklist(add_a_letter_paragraph_picklist):  # noqa
    pass


@when("I go to letters")  # noqa
def i_go_to_letters(driver, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/document-templates")


@when("I create a letter template for a document")  # noqa
def create_letter_template(driver, context, get_template_id):  # noqa
    template_page = LetterTemplates(driver)
    template_page.click_create_a_template()

    context.template_name = f"Template {utils.get_formatted_date_time_y_m_d_h_s()}"
    template_page.enter_template_name(context.template_name)
    functions.click_submit(driver)

    template_page.select_which_type_of_cases_template_can_apply_to(
        ["Standard-Individual-Export-Licence", "Open-Individual-Export-Licence"]
    )
    functions.click_submit(driver)

    template_page.select_which_type_of_decisions_template_can_apply_to(["Approve", "Proviso"])
    functions.click_submit(driver)

    template_page.select_visible_to_exporter("True")
    functions.click_submit(driver)

    template_page.select_has_signature("False")
    functions.click_submit(driver)

    template_page.click_licence_layout(get_template_id)
    functions.click_submit(driver)


@when("I add a letter paragraph to template")  # noqa
def add_two_letter_paragraphs(driver, context):  # noqa
    letter_template = LetterTemplates(driver)
    letter_template.click_add_letter_paragraph()
    context.letter_paragraph_name = letter_template.add_letter_paragraph()
    letter_template.click_add_letter_paragraphs()


@when("I preview template")  # noqa
def preview_template(driver):  # noqa
    LetterTemplates(driver).click_create_preview_button()


@when("I apply filters")  # noqa
def i_apply_filters(driver, context):  # noqa
    functions.click_apply_filters(driver)


@then("I don't see previously created application")
def dont_see_previously_created_application(driver, context):  # noqa
    case_page = CaseListPage(driver)
    functions.open_case_filters(driver)
    case_page.filter_by_case_reference(context.reference_code)
    functions.click_apply_filters(driver)
    assert context.reference_code not in driver.find_element(by=By.ID, value="main-content").text


@when("I click clear filters")  # noqa
def i_click_clear_filters(driver, context):  # noqa
    CaseListPage(driver).click_clear_filters_button()


@given("A template exists for the appropriate decision")  # noqa
def template_with_decision(context, api_test_client):  # noqa
    document_template = api_test_client.document_templates.add_template(
        api_test_client.picklists, advice_type=[context.advice_type]
    )
    context.document_template_id = document_template["id"]
    context.document_template_name = document_template["name"]


@when("I generate a document for the decision")  # noqa
def generate_decision_document(driver, context):  # noqa
    GeneratedDecisionDocuments(driver).click_generate_decision_document(context.advice_type)


@given(parsers.parse('I "{decision}" the open application good and country at all advice levels'))  # noqa
def approve_open_application_objects(context, api_test_client, decision):  # noqa
    context.advice_type = decision
    text = "abc"
    note = ""
    footnote_required = "False"
    data = [
        {
            "type": context.advice_type,
            "text": text,
            "note": note,
            "goods_type": context.goods_type["id"],
            "footnote_required": footnote_required,
        },
        {
            "type": context.advice_type,
            "text": text,
            "note": note,
            "country": context.country["code"],
            "footnote_required": footnote_required,
        },
    ]

    api_test_client.cases.create_user_advice(context.case_id, data)
    api_test_client.cases.create_team_advice(context.case_id, data)
    api_test_client.cases.create_final_advice(context.case_id, data)


@when("I approve the good country combination")  # noqa
def approve_good_country_combination(driver, context):  # noqa
    GoodCountryMatrixPage(driver).select_good_country_option(
        "approve", context.goods_type["id"], context.country["code"]
    )
    functions.click_submit(driver)


@when("I click continue on the approve open licence page")  # noqa
def approve_licence_page(driver, context):  # noqa
    page = GrantLicencePage(driver)
    context.licence_duration = page.get_duration_in_finalise_view()
    context.licence_start_date = timezone.localtime().strftime(DATE_FORMAT)
    functions.click_submit(driver)


@then("The licence information is in the second audit")  # noqa
def licence_audit(driver, context, internal_url):  # noqa
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)
    second_audit = ApplicationPage(driver).get_text_of_audit_trail_item(1)
    assert context.licence_duration in second_audit
    assert context.licence_start_date in second_audit


def select_queue(driver, queue_name, check):  # noqa
    # selects the queue from the list of checkboxes and checks/unchecks
    # depending on the input state
    queues = driver.find_elements(by=By.CLASS_NAME, value="govuk-checkboxes__item")
    target_queue = None
    for item in queues:
        label = item.find_element(by=By.XPATH, value=".//label")
        if label.text == queue_name:
            target_queue = item
            break

    assert target_queue is not None
    queue_checkbox = target_queue.find_element(by=By.XPATH, value=".//input")
    if check:
        if not queue_checkbox.is_selected():
            queue_checkbox.click()
    else:
        if queue_checkbox.is_selected():
            queue_checkbox.click()


@when(parsers.parse('I assign the case to "{queue}" queue'))  # noqa
def assign_case_to_queue(driver, queue):  # noqa
    driver.find_element(by=By.ID, value="link-change-queues").click()
    select_queue(driver, queue, True)
    functions.click_submit(driver)


@then(parsers.parse('I remove the case from "{queue}" queue'))  # noqa
def remove_case_from_queue(driver, queue):  # noqa
    driver.find_element(by=By.ID, value="link-change-queues").click()
    select_queue(driver, queue, False)
    functions.click_submit(driver)


@then(parsers.parse('I see the case is assigned to queues "{queues}"'))  # noqa
def case_assigned_to_queues(driver, queues):  # noqa
    assigned = CasePage(driver).get_assigned_queues()

    for queue in queues.split(","):
        assert queue.strip() in assigned


@then(parsers.parse('I see the case is not assigned to queues "{queues}"'))  # noqa
def case_not_assigned_to_queues(driver, queues):  # noqa
    assigned = CasePage(driver).get_assigned_queues()

    for queue in queues.split(","):
        assert queue.strip() not in assigned


@then("I see the case is not assigned to any queues")  # noqa
def case_not_assigned_to_any_queue(driver):  # noqa
    assert CasePage(driver).get_assigned_queues() == "Not assigned to any queues"


@then(parsers.parse('the flag "{flag}" is not present'))  # noqa
def flag_not_present(driver, flag):  # noqa
    flags_container = driver.find_element(by=By.ID, value="case-flags")
    el = flags_container.find_elements_by_xpath(f"//li[contains(text(), '{flag}')]")
    assert len(el) == 0


@when("I click on the notes and timeline tab")  # noqa
def case_notes_tab(driver, internal_url, context):  # noqa
    ApplicationPage(driver).go_to_cases_activity_tab(internal_url, context)


@then(parsers.parse('I see "{case_note}" as a case note'))  # noqa
def note_is_displayed(driver, case_note):  # noqa
    application_page = ApplicationPage(driver)
    assert case_note in application_page.get_text_of_case_note(0)
    assert utils.search_for_correct_date_heading_regex_in_element(
        application_page.get_text_of_case_note_date_time(0)
    ), "incorrect date format of post on case note"


@when(parsers.parse('I switch to "{team}" with queue "{queue}" and I submit the case'))
def submit_case_as_team(driver, team, queue, context, internal_url, internal_info):  # noqa
    submit_case_as_team_with_decision(driver, team, queue, None, context, internal_url, internal_info)


@when(parsers.parse('I switch to "{team}" with queue "{queue}" and I submit the case with decision "{decision}"'))
def submit_case_as_team_with_decision(driver, team, queue, decision, context, internal_url, internal_info):  # noqa
    get_profile_page(driver)
    go_to_team_edit_page(driver, team, queue)
    get_my_case_list(driver)
    i_click_application_previously_created(driver, context)
    i_assign_myself_to_case(driver, internal_info)
    im_done_button(driver)

    if decision:
        driver.find_element(by=By.XPATH, value="//span[contains(text(), 'Explain why')]").click()
        driver.find_element(by=By.XPATH, value="//textarea[@id='note']").send_keys(decision)

    submit_form(driver)
    click_on_created_application(driver, context, internal_url)
    case_page = CasePage(driver)
    case_page.change_tab(CaseTabs.DETAILS)


@then(parsers.parse('for the first good I see "{value}" for "{name}"'))
def check_first_goods_row(driver, value, name):  # noqa
    assert value == CasePage(driver).get_goods_row_with_headers(row_num=1)[name]


@then(parsers.parse('for the second good I see "{value}" for "{name}"'))
def check_second_goods_row(driver, value, name):  # noqa
    assert value == CasePage(driver).get_goods_row_with_headers(row_num=2)[name]


@then("I see the application destinations")
def i_see_destinations(driver, context):  # noqa
    destinations = [context.consignee, context.end_user, context.third_party, context.ultimate_end_user]
    destinations_table_text = CasePage(driver).get_destinations_text()

    for destination in destinations:
        assert destination["name"] in destinations_table_text


@then("I click on Notes and timeline")
def click_on_notes_and_timeline(driver):  # noqa
    ApplicationPage(driver).click_on_notes_and_timeline()


@then("I click on Product assessment")
def click_on_product_assessment(driver):  # noqa
    ApplicationPage(driver).click_on_product_assessment()


@then("I select good")  # noqa
def click_on_product_assessment(driver):  # noqa
    ApplicationPage(driver).select_a_good()


@then(
    parsers.parse('I select "{prefix}" / "{subject}" as report summary prefix / subject and regime to none and submit')
)
def fill_report_summary_select_regime_none_and_submit(driver, prefix, subject):  # noqa
    functions.select_report_summary_prefix_and_fill(driver, prefix)
    functions.select_report_summary_subject_and_fill(driver, subject)
    functions.click_regime_none(driver)
    functions.click_submit(driver)


@when("I click move case forward")  # noqa
@when("I click submit recommendation")  # noqa
@when("I click save and publish to exporter")  # noqa
def submit_form(driver):  # noqa
    functions.click_submit(driver)


@then(parsers.parse('I select the CLE "{control_code}"'))
def add_cle_value(driver, control_code):  # noqa
    add_goods_page = AddGoodPage(driver)
    add_goods_page.enter_control_list_entries(control_code)


@when("I assign myself to the case")
def i_assign_myself_to_case(driver, internal_info):  # noqa
    case_page = CasePage(driver)
    if case_page.get_assigned_case_officer() != "Not assigned":
        # remove case officer before I assign myself
        i_remove_case_officer_from_case(driver)
    # go to Assign case officer page
    case_page = CasePage(driver)
    case_page.click_assign_case_officer()
    # search for myself
    case_officer_page = CaseOfficerPage(driver)
    case_officer_page.search(internal_info["email"])
    # search for myself
    case_officer_page.select_first_user()
    functions.click_submit(driver)


@when("I remove case officer from the case")
def i_remove_case_officer_from_case(driver):  # noqa
    # go to remove case officer page
    CasePage(driver).click_remove_case_officer()
    functions.click_submit(driver)


@given(parsers.parse('I set the case status to "{status}"'))
def set_case_status(driver, status, api_test_client, context):
    api_test_client.cases.manage_case_status(api_test_client.context["case_id"], status=status.lower())


@given(parsers.parse('I create a standard draft application with "{reference}" as reference'))
def create_standard_draft_with_reference(api_test_client, context, reference):
    draft = {
        "name": reference,
        "application_type": "siel",
        "export_type": "permanent",
        "have_you_been_informed": "yes",
        "reference_number_on_information_form": "1234",
    }
    draft_id = api_test_client.applications.create_draft(draft)

    end_use_details = {
        "intended_end_use": "Research and development",
        "is_military_end_use_controls": False,
        "is_informed_wmd": False,
        "is_suspected_wmd": False,
        "is_eu_military": False,
    }
    route_of_goods = {"is_shipped_waybill_or_lading": True}
    additional_information = {"is_mod_security_approved": False}

    api_test_client.applications.add_end_use_details(draft_id=draft_id, details=end_use_details)
    api_test_client.applications.add_route_of_goods(draft_id=draft_id, route_of_goods=route_of_goods)
    api_test_client.applications.add_additional_information(draft_id=draft_id, json=additional_information)

    context.case_id = draft_id


@given(parsers.parse('I add End-user with details "{name}", "{address}", "{country}"'))
def add_end_user_to_application(api_test_client, context, name, address, country):
    party_type = "end_user"
    end_user = {
        "type": party_type,
        "name": name,
        "address": address,
        "country": country,
        "sub_type": "government",
        "website": fake.uri(),
        "signatory_name_euu": name,
        "end_user_document_available": False,
        "end_user_document_missing_reason": "document not available",
    }
    api_test_client.applications.parties.add_party(context.case_id, party_type, end_user)


@given(parsers.parse('I add Consignee with details "{name}", "{address}", "{country}"'))
def add_consignee_to_application(api_test_client, context, name, address, country):
    party_type = "consignee"
    consignee = {
        "type": party_type,
        "name": name,
        "address": address,
        "country": country,
        "sub_type": "government",
        "website": fake.uri(),
    }
    api_test_client.applications.parties.add_party(context.case_id, party_type, consignee)


@given(parsers.parse("I add a set of products to the application as json:\n{products_data}"))
def add_products_to_application(api_test_client, context, products_data):
    good_on_application_ids = []
    products = json.loads(products_data.replace("\n", ""))
    for product in products:
        data = {
            **product,
            "is_good_controlled": True,
            "is_pv_graded": "no",
            "item_category": "group2_firearms",
        }
        good = api_test_client.applications.goods.post_good(data)

        data = {
            "good_id": good["id"],
            "quantity": 64,
            "unit": "NAR",
            "value": 256.32,
            "is_good_incorporated": False,
        }
        good_on_application = api_test_client.applications.goods.add_good_to_draft(context.case_id, data)
        good_on_application_ids.append(good_on_application["id"])

    context.good_on_application_ids = good_on_application_ids


@given("the application is submitted")
def application_submitted(api_test_client, context):
    assert context.case_id
    api_test_client.applications.submit_application(context.case_id)
    context.reference_code = api_test_client.context["reference_code"]


@when(parsers.parse('I select product "{name}" to assess'))  # noqa
def select_product_name_to_assess(driver, name):
    unassessed_products = driver.find_elements(by=By.ID, value="unassessed-products")
    matching_product = [element for element in unassessed_products if name == element.text[3:]]
    assert len(matching_product) == 1

    check_box = matching_product[0].find_element(by=By.CLASS_NAME, value="govuk-checkboxes__input")
    check_box.click()


@when(parsers.parse('I assess rating as "{rating}"'))  # noqa
def assess_product_rating(driver, rating):
    ProductAssessmentPage(driver).assess_rating(rating)


@when(parsers.parse('I assess report summary prefix as "{prefix}"'))  # noqa
def assess_product_report_summary_prefix(driver, prefix):
    ProductAssessmentPage(driver).assess_report_summary_prefix(prefix)


@when(parsers.parse('I assess report summary subject as "{subject}"'))  # noqa
def assess_product_report_summary_subject(driver, subject):
    ProductAssessmentPage(driver).assess_report_summary_subject(subject)


@when(parsers.parse("I do not add any regimes"))  # noqa
def mark_regimes_as_none(driver):
    ProductAssessmentPage(driver).mark_regime_none()


@when(parsers.parse('I add assessment note as "{comment}"'))  # noqa
def assess_product_assessment_note(driver, comment):
    ProductAssessmentPage(driver).add_assessment_note(comment)


@when(parsers.parse("I submit my assessment for this product"))  # noqa
def submit_product_assessment(driver):
    functions.click_submit(driver)


@then(parsers.parse('I see "{name}" in the list of assessed products'))  # noqa
def check_product_in_assesse_products(driver, name):
    ProductAssessmentPage(driver).check_product_assessment_status(name)
