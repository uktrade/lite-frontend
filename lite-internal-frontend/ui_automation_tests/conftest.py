import os
from django.conf import settings
from pytest_bdd import given, when, then, parsers

from pages.advice import FinalAdvicePage, TeamAdvicePage
from pages.case_page import CasePage, CaseTabs
from pages.goods_queries_pages import GoodsQueriesPages

from ui_automation_tests.fixtures.env import environment  # noqa
from ui_automation_tests.fixtures.add_a_flag import (  # noqa
    add_case_flag,
    add_good_flag,
    add_organisation_flag,
    add_destination_flag,
    get_flag_of_level,
)
from ui_automation_tests.fixtures.add_queue import add_queue  # noqa
from ui_automation_tests.fixtures.add_a_document_template import (  # noqa
    add_a_document_template,
    get_template_id,
)
from ui_automation_tests.fixtures.add_a_picklist import (  # noqa
    add_a_letter_paragraph_picklist,
    add_an_ecju_query_picklist,
    add_a_proviso_picklist,
    add_a_standard_advice_picklist,
    add_a_report_summary_picklist,
)
from ui_automation_tests.pages.generate_document_page import GeneratedDocument
from ui_automation_tests.shared.fixtures.apply_for_application import *  # noqa
from ui_automation_tests.shared.fixtures.driver import driver  # noqa
from ui_automation_tests.shared.fixtures.sso_sign_in import sso_sign_in  # noqa
from ui_automation_tests.shared.fixtures.core import (  # noqa
    context,
    api_test_client,
    exporter_info,
    internal_info,
    api_client,
)
from ui_automation_tests.shared.fixtures.urls import internal_url, sso_sign_in_url, api_url  # noqa

import shared.tools.helpers as utils
from pages.shared import Shared
from pages.case_list_page import CaseListPage
from pages.application_page import ApplicationPage

from ui_automation_tests.shared.tools.helpers import get_formatted_date_time_y_m_d_h_s


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
    parser.addoption(
        "--sso_sign_in_url", action="store", default=str(os.environ.get("AUTHBROKER_URL")) + "/login", help="url"
    )

    if env.lower() == "local":
        parser.addoption(
            "--internal_url", action="store", default="http://localhost:" + str(os.environ.get("PORT")), help="url"
        )

        # Get LITE API URL.
        lite_api_url = os.environ.get("LOCAL_LITE_API_URL", os.environ.get("LITE_API_URL"),)
        parser.addoption(
            "--lite_api_url", action="store", default=lite_api_url, help="url",
        )

    elif env == "demo":
        raise NotImplementedError("This is the demo environment - Try another environment instead")
    else:
        parser.addoption(
            "--internal_url",
            action="store",
            default="https://internal.lite.service." + env + ".uktrade.digital/",
            help="url",
        )
        parser.addoption(
            "--lite_api_url",
            action="store",
            default="https://lite-api-" + env + ".london.cloudapps.digital/",
            help="url",
        )


# Create driver and url command line adoption
def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = " {0}_{1}".format(class_name, "error")
        try:
            utils.save_screenshot(node.funcargs.get("driver"), name)
        except Exception:  # noqa
            pass


@when("I go to the internal homepage")  # noqa
def when_go_to_internal_homepage(driver, internal_url):  # noqa
    driver.get(internal_url)


@given("I go to internal homepage")  # noqa
def go_to_internal_homepage(driver, internal_url):  # noqa
    driver.get(internal_url)


@given("I sign in to SSO or am signed into SSO")  # noqa
def sign_into_sso(driver, sso_sign_in):  # noqa
    pass


@when("I go to application previously created")  # noqa
def click_on_created_application(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.case_id)


@given("I create standard application or standard application has been previously created")  # noqa
def create_app(driver, apply_for_standard_application):  # noqa
    pass


@given("I create open application or open application has been previously created")  # noqa
def create_open_app(driver, apply_for_open_application):  # noqa
    pass


@when("I click continue")  # noqa
def i_click_continue(driver):  # noqa
    Shared(driver).click_submit()


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
def see_queue_in_queue_list(driver, context):  # noqa
    case_page = CaseListPage(driver)
    case_page.click_show_filters_link()
    case_page.filter_by_case_reference(context.reference_code)
    case_page.click_apply_filters_button()
    assert driver.find_element_by_id(context.case_id).is_displayed()


@when("I show filters")  # noqa
def i_show_filters(driver, context):  # noqa
    CaseListPage(driver).click_show_filters_link()


@when("I go to users")  # noqa
def go_to_users(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/users/")


@given("I create a clc query")  # noqa
def create_clc_query(driver, apply_for_clc_query, context):  # noqa
    pass


@when("I go to the case list page")  # noqa
def case_list_page(driver, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/")


@then("I should see my case in the cases list")  # noqa
def case_in_cases_list(driver, context):  # noqa
    context.case_row = CaseListPage(driver).get_case_row(context.case_id)
    assert context.reference_code in context.case_row.text


@then("I should see my case SLA")  # noqa
def case_sla(driver, context):  # noqa
    assert CaseListPage(driver).get_case_row_sla(context.case_row) == "0"


@then("I see the case page")  # noqa
def i_see_the_case_page(driver, context):  # noqa
    assert context.reference_code in driver.find_element_by_id(ApplicationPage.HEADING_ID).text


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


@when("I go to the documents tab")  # noqa
def click_documents(driver):  # noqa
    CasePage(driver).change_tab(CaseTabs.DOCUMENTS)


@when("I click I'm done")  # noqa
def im_done_button(driver):  # noqa
    ApplicationPage(driver).click_im_done_button()


@when("I go to my work queue")  # noqa
def work_queue(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/" + context.queue_id)


@then("My case is not in the queue")  # noqa
def no_cases_in_queue(driver, context):  # noqa
    assert context.case_id not in Shared(driver).get_text_of_cases_form()


@given("a queue has been created")  # noqa
def create_queue(context, api_test_client):  # noqa
    api_test_client.queues.add_queue("queue " + get_formatted_date_time_y_m_d_h_s())
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


@when("I go to the final advice page by url")  # noqa
def final_advice_page(driver, context, internal_url):  # noqa
    driver.get(
        internal_url.rstrip("/")
        + "/queues/00000000-0000-0000-0000-000000000001/cases/"
        + context.case_id
        + "/final-advice/"
    )


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
    query_page = GoodsQueriesPages(driver)
    query_page.click_is_good_controlled(controlled)
    query_page.type_in_to_control_list_entry(control_list_entry)
    context.goods_control_list_entry = control_list_entry
    query_page.choose_report_summary()
    context.report = report
    query_page.enter_a_comment(comment)
    context.comment = comment
    Shared(driver).click_submit()
