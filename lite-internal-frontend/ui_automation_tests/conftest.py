import datetime
import os
from pytest_bdd import given, when, then, parsers

from fixtures.core import context, driver, sso_login_info, invalid_username, new_cases_queue_id
from fixtures.urls import internal_url, sso_sign_in_url, api_url
from fixtures.apply_for_application import apply_for_standard_application, apply_for_clc_query
from fixtures.sign_in_to_sso import sign_in_to_internal_sso

import helpers.helpers as utils
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr
from pages.flags_pages import FlagsPages
from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.case_list_page import CaseListPage
from pages.application_page import ApplicationPage
from pages.queues_pages import QueuesPages

# Screenshot in case of any test failure


def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        # utils.save_screenshot(node.funcargs.get("driver"), class_name)


# Create driver and url command line adoption
def pytest_addoption(parser):
    env = str(os.environ.get('ENVIRONMENT'))
    if env == 'None':
        env = "dev"

    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")
    
    if env == 'local':
        parser.addoption("--internal_url", action="store", default="http://localhost:8080", help="url")
        parser.addoption("--lite_api_url", action="store", default="http://localhost:8100", help="url")
    else:
        parser.addoption("--internal_url", action="store", default="https://internal.lite.service." + env + ".uktrade.io/", help="url")
        parser.addoption("--lite_api_url", action="store", default="https://lite-api-" + env + ".london.cloudapps.digital/", help="url")


@when('I go to the internal homepage')
def when_go_to_internal_homepage(driver, internal_url):
    driver.get(internal_url)


@given('I go to internal homepage')
def go_to_internal_homepage(driver, internal_url, sign_in_to_internal_sso):
    driver.get(internal_url)


@given('I sign in to SSO or am signed into SSO')
def sign_into_sso(driver, sign_in_to_internal_sso):
    pass


@when('I go to internal homepage and sign in')
def go_to_internal_homepage_sign_in(driver, internal_url, sso_sign_in_url, sso_login_info):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_login_info['email'])
    driver.find_element_by_name("password").send_keys(sso_login_info['password'])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@when('I go to application previously created')
def click_on_created_application(driver, context, internal_url):
    driver.get(internal_url.rstrip('/') + '/cases/' + context.case_id)


@given('I create application or application has been previously created')
def create_app(driver, apply_for_standard_application):
    pass


@when('I create application or application has been previously created')
def create_app_when(driver, apply_for_standard_application):
    pass


@given('I create clc query or clc query has been previously created')
def create_clc(driver, apply_for_clc_query):
    pass


@when('I click submit button')
def click_on_submit_button(driver):
    shared = Shared(driver)
    shared.click_submit()


@when('I refresh the page')
def I_refresh_the_page(driver):
    driver.refresh()


@then(parsers.parse('I see error message "{expected_error}"'))
def error_message_shared(driver, expected_error):
    shared = Shared(driver)
    assert expected_error in shared.get_text_of_error_message(0), "expected error message is not displayed"


@when('I click continue')
def i_click_continue(driver):
    driver.find_element_by_css_selector("button[type*='submit']").click()


@when('I go to flags')
def go_to_flags(driver):
    header = HeaderPage(driver)

    header.click_lite_menu()
    header.click_flags()


@when(parsers.parse('I add a flag called "{flag_name}" at level "{flag_level}"'))
def add_a_flag(driver, flag_name, flag_level, context):
    flags_page = FlagsPages(driver)
    shared = Shared(driver)
    utils.get_unformatted_date_time()
    flags_page.click_add_a_flag_button()
    if flag_name == " ":
        context.flag_name = flag_name
    else:
        extra_string = str(utils.get_unformatted_date_time())
        extra_string = extra_string[(len(extra_string))-7:]
        context.flag_name = flag_name + extra_string
    flags_page.enter_flag_name(context.flag_name)
    flags_page.select_flag_level(flag_level)
    shared.click_submit()


@when('I go to users')
def go_to_users(driver):
    header = HeaderPage(driver)

    header.open_users()


@then('I see the clc-case previously created')
def assert_case_is_present(driver, apply_for_clc_query, context):
    case_list_page = CaseListPage(driver)
    assert case_list_page.assert_case_is_present(context.case_id), "clc case ID is not present on page"


@when('I create a clc_query')
def create_clc_query(driver, apply_for_clc_query, context):
    pass


@when('I click on the clc-case previously created')
def click_on_clc_case_previously_created(driver, context):
    case_list_page = CaseListPage(driver)
    assert case_list_page.assert_case_is_present(context.case_id)
    case_list_page.click_on_href_within_cases_table(context.case_id)


@when('I click progress application')
def click_post_note(driver):
    application_page = ApplicationPage(driver)
    application_page.click_progress_application()


@when(parsers.parse('I select status "{status}" and save'))
def select_status_save(driver, status, context):
    application_page = ApplicationPage(driver)
    application_page.select_status(status)
    context.status = status
    context.date_time_of_update = utils.get_formatted_date_time_h_m_pm_d_m_y()
    driver.find_element_by_css_selector(".govuk-button").click()


@when('I click on new queue in dropdown')
def new_queue_shown_in_dropdown(driver, context):
    driver.find_element_by_id('queue-title').click()
    elements = driver.find_elements_by_css_selector('.lite-dropdown .lite-dropdown--item')
    for idx, element in enumerate(elements):
        if element.text == context.queue_name:
            driver.execute_script("document.getElementsByClassName('lite-dropdown--item')[" + str(idx) + "].scrollIntoView(true);")
            element.click()
            break


@then('there are no cases shown')
def no_cases_shown(driver):
    assert 'There are no new cases to show.' in QueuesPages(driver).get_no_cases_text()


