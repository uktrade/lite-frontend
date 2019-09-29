import os

from pytest_bdd import given, when, then, parsers

from fixtures.core import context, driver, sso_login_info, invalid_username, new_cases_queue_id, sso_users_name # noqa
from fixtures.urls import internal_url, sso_sign_in_url, api_url # noqa
from fixtures.apply_for_application import apply_for_standard_application, apply_for_clc_query, apply_for_eua_query # noqa
from fixtures.sign_in_to_sso import sign_in_to_internal_sso # noqa
from fixtures.add_a_flag import add_uae_flag, add_suspicious_flag # noqa
from fixtures.add_queue import add_queue # noqa
from fixtures.add_a_team import add_a_team # noqa
from fixtures.add_a_picklist import add_an_ecju_query_picklist, add_a_proviso_picklist, add_a_standard_advice_picklist, add_a_report_summary_picklist # noqa

import helpers.helpers as utils
from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.case_list_page import CaseListPage
from pages.application_page import ApplicationPage
from pages.queues_pages import QueuesPages
from core.builtins.custom_tags import reference_code

# Screenshot in case of any test failure


def pytest_addoption(parser):
    env = str(os.environ.get('ENVIRONMENT'))
    if env == 'None':
        env = "dev"

    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")

    if env.lower() == 'local':
        parser.addoption("--internal_url", action="store", default="http://localhost:8200", help="url")
        parser.addoption("--lite_api_url", action="store", default="http://localhost:8100", help="url")
    elif env == 'demo':
        raise Exception("This is the demo environment - Try another environment instead")
    else:
        parser.addoption("--internal_url", action="store",
                         default="https://internal.lite.service." + env + ".uktrade.io/", help="url")
        parser.addoption("--lite_api_url", action="store",
                         default="https://lite-api-" + env + ".london.cloudapps.digital/", help="url")


# Create driver and url command line adoption
def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = " {0}_{1}".format(class_name, "error")
        try:
            utils.save_screenshot(node.funcargs.get("driver"), name)
        except Exception: # noqa
            pass


@when('I go to the internal homepage') # noqa
def when_go_to_internal_homepage(driver, internal_url):
    driver.get(internal_url)


@given('I go to internal homepage') # noqa
def go_to_internal_homepage(driver, internal_url, sign_in_to_internal_sso):
    driver.get(internal_url)


@given('I sign in to SSO or am signed into SSO') # noqa
def sign_into_sso(driver, sign_in_to_internal_sso):
    pass


@when('I go to application previously created') # noqa
def click_on_created_application(driver, context, internal_url):
    driver.get(internal_url.rstrip('/') + '/cases/' + context.case_id)


@when('I go to end user advisory previously created') # noqa
def click_on_created_eua(driver, context):
    driver.find_element_by_link_text(reference_code(context.eua_id)).click()


@when('I go to clc query previously created') # noqa
def click_on_created_application(driver, context, internal_url):
    driver.get(internal_url.rstrip('/') + '/cases/' + context.clc_case_id)


@given('I create application or application has been previously created') # noqa
def create_app(driver, apply_for_standard_application):
    pass


@given('I create clc query or clc query has been previously created') # noqa
def create_clc(driver, apply_for_clc_query):
    pass


@given('I create eua query or eua query has been previously created') # noqa
def create_eua(driver, apply_for_eua_query):
    pass


@then(parsers.parse('I see error message "{expected_error}"')) # noqa
def error_message_shared(driver, expected_error):
    shared = Shared(driver)
    assert expected_error in shared.get_text_of_error_message(0), "expected error message is not displayed"


@when('I click continue') # noqa
def i_click_continue(driver):
    Shared(driver).click_submit()


@when('I click back') # noqa
def i_click_back(driver):
    Shared(driver).click_back()


@given('I go to flags') # noqa
def go_to_flags(driver, internal_url, sign_in_to_internal_sso):
    driver.get(internal_url.rstrip("/")+"/flags")


@when('I go to users') # noqa
def go_to_users(driver):
    header = HeaderPage(driver)
    header.open_users()


@then('I see the clc-case previously created') # noqa
def assert_case_is_present(driver, apply_for_clc_query, context):
    case_list_page = CaseListPage(driver)
    assert case_list_page.assert_case_is_present(context.clc_case_id), "clc case ID is not present on page"


@when('I create a clc_query') # noqa
def create_clc_query(driver, apply_for_clc_query, context):
    pass


@when('I click on the clc-case previously created') # noqa
def click_on_clc_case_previously_created(driver, context):
    case_list_page = CaseListPage(driver)
    assert case_list_page.assert_case_is_present(context.case_id)
    case_list_page.click_on_href_within_cases_table(context.case_id)


@when('I click progress application') # noqa
def click_post_note(driver):
    application_page = ApplicationPage(driver)
    application_page.click_progress_application()


@when(parsers.parse('I select status "{status}" and save')) # noqa
def select_status_save(driver, status, context):
    application_page = ApplicationPage(driver)
    application_page.select_status(status)
    context.status = status
    context.date_time_of_update = utils.get_formatted_date_time_h_m_pm_d_m_y()
    Shared(driver).click_submit()


@when('I click on new queue in dropdown') # noqa
def new_queue_shown_in_dropdown(driver, context):
    CaseListPage(driver).click_on_queue_name(context.queue_name)


@then('there are no cases shown') # noqa
def no_cases_shown(driver):
    assert 'There are no new cases to show.' in QueuesPages(driver).get_no_cases_text(), "There are cases shown in the newly created queue."


@when(parsers.parse('I click on the "{queue_name}" queue in dropdown')) # noqa
def system_queue_shown_in_dropdown(driver, queue_name):
    CaseListPage(driver).click_on_queue_name(queue_name)


@when(parsers.parse('I click on the added queue in dropdown')) # noqa
def system_queue_shown_in_dropdown(driver, context):
    CaseListPage(driver).click_on_queue_name(context.queue_name)


@when('I enter in queue name Review') # noqa
def add_a_queue(driver, context, add_queue):
    pass


@when('I go to queues via menu') # noqa
def go_to_queues_via_menu(driver):
    HeaderPage(driver).click_lite_menu()
    HeaderPage(driver).click_queues()


@given('I go to queues') # noqa
def go_to_queues(driver, sign_in_to_internal_sso, internal_url):
    driver.get(internal_url.rstrip('/') + '/queues/')


@when('I add case to newly created queue') # noqa
def move_case_to_new_queue(driver, context):
    ApplicationPage(driver).click_move_case_button()
    if not driver.find_element_by_id(context.queue_name).is_selected():
        driver.find_element_by_id(context.queue_name).click()
    Shared(driver).click_submit()
