import os

from pytest_bdd import given, when, then, parsers
from selenium.common.exceptions import NoSuchElementException

from pages.goods_queries_pages import GoodsQueriesPages  # noqa
from pages.organisation_page import OrganisationPage

from ui_automation_tests.fixtures.env import environment  # noqa
from ui_automation_tests.fixtures.add_a_flag import (  # noqa
    add_uae_flag,
    add_suspicious_flag,
    add_organisation_suspicious_flag,
    add_new_flag,
)
from ui_automation_tests.fixtures.add_queue import add_queue  # noqa
from ui_automation_tests.fixtures.add_a_team import add_a_team  # noqa
from ui_automation_tests.fixtures.add_a_document_template import (  # noqa
    add_a_document_template,
    get_template_id,
    get_licence_template_id,
)
from ui_automation_tests.fixtures.add_a_picklist import (  # noqa
    add_a_letter_paragraph_picklist,
    add_an_ecju_query_picklist,
    add_a_proviso_picklist,
    add_a_standard_advice_picklist,
    add_a_report_summary_picklist,
)
from ui_automation_tests.shared.fixtures.apply_for_application import *  # noqa
from ui_automation_tests.shared.fixtures.driver import driver  # noqa
from ui_automation_tests.shared.fixtures.sso_sign_in import sso_sign_in  # noqa
from ui_automation_tests.shared.fixtures.core import (  # noqa
    context,
    seed_data_config,
    exporter_info,
    internal_info,
)
from ui_automation_tests.shared.fixtures.urls import internal_url, sso_sign_in_url, api_url  # noqa

import shared.tools.helpers as utils
from pages.assign_flags_to_case import CaseFlagsPages
from pages.shared import Shared
from pages.case_list_page import CaseListPage
from pages.application_page import ApplicationPage
from pages.queues_pages import QueuesPages


def pytest_addoption(parser):
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
def go_to_internal_homepage(driver, internal_url, sso_sign_in):  # noqa
    driver.get(internal_url)


@given("I sign in to SSO or am signed into SSO")  # noqa
def sign_into_sso(driver, sso_sign_in):  # noqa
    pass


@when("I go to application previously created")  # noqa
def click_on_created_application(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/cases/" + context.case_id)


@when("I go to open application previously created")  # noqa
def click_on_created_application(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/cases/" + context.case_id)


@when("I go to end user advisory previously created")  # noqa
def click_on_created_eua(driver, context):  # noqa
    utils.find_paginated_item_by_link_text(context.eua_reference_code, driver).click()


@given("I create application or application has been previously created")  # noqa
def create_app(driver, apply_for_standard_application):  # noqa
    pass


@given("I create open application or open application has been previously created")  # noqa
def create_open_app(driver, apply_for_open_application):  # noqa
    pass


@when("I click continue")  # noqa
def i_click_continue(driver):  # noqa
    Shared(driver).click_submit()


@when("I go to flags")  # noqa
def go_to_flags(driver, internal_url, sso_sign_in):  # noqa
    driver.get(internal_url.rstrip("/") + "/flags")


@when("I click progress application")  # noqa
def click_post_note(driver):  # noqa
    application_page = ApplicationPage(driver)
    application_page.click_progress_application()


@when(parsers.parse('I select status "{status}" and save'))  # noqa
def select_status_save(driver, status, context):  # noqa
    application_page = ApplicationPage(driver)
    application_page.select_status(status)
    context.status = status
    context.date_time_of_update = utils.get_formatted_date_time_h_m_pm_d_m_y()
    Shared(driver).click_submit()


@when("I click on new queue in dropdown")  # noqa
def new_queue_shown_in_dropdown(driver, context):  # noqa
    CaseListPage(driver).click_on_queue_name(context.queue_name)


@when(parsers.parse('I click on the "{queue_name}" queue in dropdown'))  # noqa
def system_queue_shown_in_dropdown(driver, queue_name):  # noqa
    CaseListPage(driver).click_on_queue_name(queue_name)


@when("I enter in queue name Review")  # noqa
def add_a_queue(driver, context, add_queue):  # noqa
    pass


@when("I go to queues")  # noqa
def go_to_queues(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/")


@when("I add case to newly created queue")  # noqa
def move_case_to_new_queue(driver, context):  # noqa
    ApplicationPage(driver).click_move_case_button()
    if not driver.find_element_by_id(context.queue_name).is_selected():
        driver.find_element_by_id(context.queue_name).click()
    Shared(driver).click_submit()


@when("I select previously created flag")  # noqa
def assign_flags_to_case(driver, context):  # noqa
    case_flags_pages = CaseFlagsPages(driver)
    case_flags_pages.select_flag(context.flag_name)
    shared = Shared(driver)
    shared.click_submit()


@given("I create report summary picklist")  # noqa
def add_report_summary_picklist(add_a_report_summary_picklist):  # noqa
    pass


@then("I see the added flags on the queue")  # noqa
def added_flags_on_queue(driver, context):  # noqa
    elements = Shared(driver).get_rows_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.case_id, complete_match=False)
    driver.set_timeout_to(0)
    try:
        if elements[no].find_element_by_css_selector(".lite-accordian-table__chevron svg").is_displayed():
            element = elements[no].find_element_by_css_selector(".lite-accordian-table__chevron")
            element.click()
    except NoSuchElementException:
        pass
    driver.set_timeout_to(10)
    assert context.flag_name in elements[no].text


@then("I see previously created application")  # noqa
def see_queue_in_queue_list(driver, context):  # noqa
    assert QueuesPages(driver).is_case_on_the_list(context.case_id) == 1, (
        "previously created application is not displayed " + context.case_id
    )


@when("I add a flag called Suspicious at level Organisation")  # noqa
def add_a_suspicious_flag(driver, add_organisation_suspicious_flag):  # noqa
    pass


@when("I go to the organisation which submitted the case")  # noqa
def go_to_the_organisation_which_submitted_the_case(driver):  # noqa
    ApplicationPage(driver).go_to_organisation()


@when("I click the edit flags link")  # noqa
def go_to_edit_flags(driver):  # noqa
    OrganisationPage(driver).click_edit_organisation_flags()


@when(parsers.parse('filter case type has been changed to "{case_type}"'))  # noqa
def filter_status_change(driver, context, case_type):  # noqa
    CaseListPage(driver).select_filter_case_type_from_dropdown(case_type)
    CaseListPage(driver).click_apply_filters_button()


@when("I show filters")  # noqa
def i_show_filters(driver, context):  # noqa
    CaseListPage(driver).click_show_filters_link()


@when("I go to users")  # noqa
def go_to_users(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/users/")


@when(  # noqa
    parsers.parse(
        'I respond "{controlled}", "{control_list_entry}", "{report}", "{comment}" and click continue'
    )  # noqa
)  # noqa
def enter_response(driver, controlled, control_list_entry, report, comment):  # noqa
    clc_query_page = GoodsQueriesPages(driver)
    clc_query_page.click_is_good_controlled(controlled)
    clc_query_page.type_in_to_control_list_entry(control_list_entry)
    clc_query_page.choose_report_summary(report)
    clc_query_page.enter_a_comment(controlled)
    Shared(driver).click_submit()


@when("I add a flag called UAE at level Case")  # noqa
def add_a_flag(driver, add_uae_flag):  # noqa
    pass


@then("the status has been changed in the application")  # noqa
def status_has_been_changed_in_header(driver, context, internal_info):  # noqa
    application_page = ApplicationPage(driver)
    if context.status.lower() == "under review":
        assert "updated the status to: " + "Under review" in application_page.get_text_of_audit_trail_item(
            0
        ), "status has not been shown as approved in audit trail"
    elif context.status.lower() == "withdrawn":
        assert "updated the status to: " + context.status in application_page.get_text_of_audit_trail_item(
            0
        ), "status has not been shown as approved in audit trail"
    else:
        assert "updated the status to " + context.status.lower() in application_page.get_text_of_audit_trail_item(
            0
        ), "status has not been shown as approved in audit trail"

    assert utils.search_for_correct_date_regex_in_element(
        application_page.get_text_of_activity_dates(0)
    ), "date is not displayed after status change"
    assert (
        application_page.get_text_of_activity_users(0) == internal_info["name"]
    ), "user who has made the status change has not been displayed correctly"
