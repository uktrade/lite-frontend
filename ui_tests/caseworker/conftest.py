from django.utils import timezone
from pytest_bdd import given, when, then, parsers
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from core.constants import CaseStatusEnum
from ui_tests.caseworker.pages.advice import FinalAdvicePage, TeamAdvicePage
from ui_tests.caseworker.pages.case_page import CasePage, CaseTabs
from ui_tests.caseworker.pages.goods_queries_pages import StandardGoodsReviewPages, OpenGoodsReviewPages
from ui_tests.caseworker.pages.teams_pages import TeamsPages
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
from tests_common.fixtures.apply_for_application import *  # noqa
from tests_common.fixtures.driver import driver  # noqa
from tests_common.fixtures.sso_sign_in import sso_sign_in  # noqa
from tests_common.fixtures.core import (  # noqa
    context,
    api_test_client,
    exporter_info,
    internal_info,
    api_client,
)
from tests_common.fixtures.urls import internal_url, sso_sign_in_url, api_url  # noqa

import tests_common.tools.helpers as utils
from ui_tests.caseworker.pages.case_list_page import CaseListPage
from ui_tests.caseworker.pages.application_page import ApplicationPage
from tests_common.helpers import applications


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
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.case_id)


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
    product_table = driver.find_element_by_id("table-goods")
    name_element = product_table.find_element_by_xpath("//tbody/tr/td[3]")
    rating_element = product_table.find_element_by_xpath("//tbody/tr/td[6]")
    assert name_element.text == product_name
    assert rating_element.text == clc_rating


@then(parsers.parse('I check the product part number is "{part_number}"'))
def check_product_part_number(driver, part_number):  # noqa
    product_table = driver.find_element_by_class_name("govuk-table")
    pn_element = product_table.find_element_by_xpath("//tbody/tr[4]/td")
    assert pn_element.text == part_number


@then(parsers.parse('I check the product annual report summary is "{report_summary}"'))
def check_product_report_summary(driver, report_summary):  # noqa
    product_table = driver.find_element_by_id("table-goods")
    summary_element = product_table.find_element_by_xpath("//tbody/tr/td[9]")
    assert summary_element.text == report_summary


@then(parsers.parse('I should see "{timeline_text}" appear in the timeline'))
def check_timeline(driver, timeline_text):  # noqa
    assert timeline_text in Shared(driver).get_audit_trail_text()


@given("I create open application or open application has been previously created")  # noqa
def create_open_app(driver, apply_for_open_application):  # noqa
    pass


@given("I prepare the application for final review")
def prepare_for_final_review(driver, api_test_client):  # noqa
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
        control_list_entries=["ML1a"],
        is_good_controlled=True,
        report_summary="ARS",
    )
    api_test_client.cases.manage_case_status(
        api_test_client.context["case_id"], status=CaseStatusEnum.UNDER_FINAL_REVIEW
    )


@when("I click save and continue")
@when("I click save")
@when("I click preview")
@when("I click confirm")
@when("I click continue")
@when("I click submit")
def submit_form(driver):  # noqa
    Shared(driver).click_submit()
    # handle case when scenario clicks submit in consecutive steps: there is a race condition resulting in the same
    # submit button being clicked for each step
    time.sleep(2)


@when(parsers.parse('I click "{button_text}"'))
def click_button_with_text(driver, button_text):  # noqa
    driver.find_element(
        by=By.XPATH,
        value=(
            f"//button[contains(@class, 'govuk-button') and contains(text(), '{button_text}')] "
            f"| //a[contains(@class, 'govuk-button') and contains(text(), '{button_text}')]"
        ),
    ).click()


@when("I click back")
def click_back_link(driver):  # noqa
    driver.find_element_by_link_text("Back").click()


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
    if not driver.find_element_by_id(context.queue_name.replace(" ", "-")).is_selected():
        driver.find_element_by_id(context.queue_name.replace(" ", "-")).click()
    Shared(driver).click_submit()


@given("I create report summary picklist")  # noqa
def add_report_summary_picklist(add_a_report_summary_picklist):  # noqa
    pass


@then("I see previously created application")  # noqa
def should_see_previously_created_application(driver, context):  # noqa
    case_page = CaseListPage(driver)
    functions.try_open_filters(driver)
    case_page.click_clear_filters_button()
    case_page = CaseListPage(driver)
    functions.try_open_filters(driver)
    case_page.filter_by_case_reference(context.reference_code)
    functions.click_apply_filters(driver)
    assert driver.find_element_by_id(context.case_id).is_displayed()


@when("I click on show filters")
def i_show_filters(driver):  # noqa
    Shared(driver).try_open_filters()


@when(parsers.parse('I click on "{tab_name}" tab'))
def i_click_on_case_details_tab(driver, tab_name):  # noqa
    tabs = driver.find_element_by_class_name("lite-tabs")
    target = tabs.find_element_by_link_text(tab_name)
    target.click()


@when(parsers.parse('I filter by application type "{application_type}"'))
def filter_by_application_type(driver, application_type):  # noqa
    CaseListPage(driver).select_filter_case_type_from_dropdown(application_type)
    functions.click_apply_filters(driver)


@when("I go to users")  # noqa
def go_to_users(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/users/")


@given("I create a clc query")  # noqa
def create_clc_query(driver, apply_for_clc_query, context):  # noqa
    pass


@when("I go to the case list page")  # noqa
def case_list_page(driver, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/")


@when("I go to my profile page")  # noqa
def get_profile_page(driver):  # noqa
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.ID, "link-profile"))).click()


@when(parsers.parse('I change my team to "{team}" and default queue to "{queue}"'))  # noqa
def go_to_team_edit_page(driver, team, queue):  # noqa
    # we should already be on the profile page
    driver.find_element_by_id("link-edit-team").click()
    teams_page = TeamsPages(driver)
    teams_page.select_team_from_dropdown(team)
    teams_page.select_default_queue_from_dropdown(queue)
    functions.click_submit(driver)


@when("I go to my case list")  # noqa
def get_my_case_list(driver):  # noqa
    """
    Clicks on the menu and selects Cases
    Depending on team, default queue the list of cases will be different
    """
    driver.find_element_by_id("link-menu").click()
    driver.find_element_by_link_text("Cases").click()


@when("I click the application previously created")
def i_click_application_previously_created(driver, context):  # noqa
    case_list_page = CaseListPage(driver)
    functions.try_open_filters(driver)
    case_list_page.click_clear_filters_button()
    functions.try_open_filters(driver)
    case_list_page.filter_by_case_reference(context.reference_code)
    functions.click_apply_filters(driver)
    case_list_page.click_on_case(context.case_id)


@when(parsers.parse('I switch to queue "{queue}"'))  # noqa
def switch_queue_dropdown(driver, queue):  # noqa
    driver.find_element_by_id("link-queue").click()
    queues = driver.find_element_by_id("queues")
    queues.find_element_by_xpath(f"//a[contains(text(), '{queue}')]").click()


@then("I should see my case in the cases list")  # noqa
def case_in_cases_list(driver, context):  # noqa
    case_page = CaseListPage(driver)
    functions.try_open_filters(driver)
    case_page.click_clear_filters_button()
    case_page = CaseListPage(driver)
    functions.try_open_filters(driver)
    case_page.filter_by_case_reference(context.reference_code)
    functions.click_apply_filters(driver)
    context.case_row = CaseListPage(driver).get_case_row(context.case_id)
    assert context.reference_code in context.case_row.text


@then("I should see there are no new cases")
def no_new_cases(driver, context):  # noqa
    case_page = CaseListPage(driver)
    functions.try_open_filters(driver)
    case_page.click_clear_filters_button()
    case_page = CaseListPage(driver)
    functions.try_open_filters(driver)
    case_page.filter_by_case_reference(context.reference_code)
    functions.click_apply_filters(driver)
    assert "There are no new cases" in driver.find_element_by_id("form-cases").text


@then("I should see my case SLA")  # noqa
def case_sla(driver, context):  # noqa
    assert CaseListPage(driver).get_case_row_sla(context.case_row) == "0"


@then("I see the case page")  # noqa
def i_see_the_case_page(driver, context):  # noqa
    assert context.reference_code in driver.find_element_by_id(ApplicationPage.HEADING_ID).text


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


@when(
    parsers.parse('I respond "{controlled}", "{control_list_entry}", "{report}", "{comment}" and click submit')
)  # noqa
def click_continue(driver, controlled, control_list_entry, report, comment, context):  # noqa
    is_standard = "SIEL" in context.reference_code
    controlled = controlled == "yes"
    query_page = StandardGoodsReviewPages(driver) if is_standard else OpenGoodsReviewPages(driver)

    query_page.click_is_good_controlled(controlled)
    query_page.type_in_to_control_list_entry(control_list_entry)
    context.goods_control_list_entry = control_list_entry
    query_page.enter_ars(report)
    context.report = report
    query_page.enter_a_comment(comment)
    context.comment = comment
    query_page.click_submit()


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
def expand_details(driver, details_text):  # noqa
    driver.find_element_by_xpath(
        f"//details[@class='govuk-details']/summary/span[contains(text(), '{details_text}')]"
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
    functions.try_open_filters(driver)
    case_page.filter_by_case_reference(context.reference_code)
    functions.click_apply_filters(driver)
    assert context.reference_code not in driver.find_element_by_id("main-content").text


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
    queues = driver.find_elements_by_class_name("govuk-checkboxes__item")
    target_queue = None
    for item in queues:
        label = item.find_element_by_xpath(".//label")
        if label.text == queue_name:
            target_queue = item
            break

    assert target_queue is not None
    queue_checkbox = target_queue.find_element_by_xpath(".//input")
    if check:
        if not queue_checkbox.is_selected():
            queue_checkbox.click()
    else:
        if queue_checkbox.is_selected():
            queue_checkbox.click()


@when(parsers.parse('I assign the case to "{queue}" queue'))  # noqa
def case_assigned_to_queue(driver, queue):  # noqa
    driver.find_element_by_id("link-change-queues").click()
    select_queue(driver, queue, True)
    functions.click_submit(driver)


@then(parsers.parse('I remove the case from "{queue}" queue'))  # noqa
def case_removed_from_queue(driver, queue):  # noqa
    driver.find_element_by_id("link-change-queues").click()
    select_queue(driver, queue, False)
    functions.click_submit(driver)


@then(parsers.parse("I see the case is not assigned to any queues"))  # noqa
def case_not_assigned_to_any_queue(driver, queue):  # noqa
    assert CasePage(driver).get_assigned_queues() == "Not assigned to any queues"


@then(parsers.parse('the flag "{flag}" is not present'))  # noqa
def flag_not_present(driver, flag):  # noqa
    flags_container = driver.find_element_by_id("case-flags")
    el = flags_container.find_elements_by_xpath(f"//li[contains(text(), '{flag}')]")
    assert len(el) == 0
