import os
from pytest_bdd import given, when, then, parsers

from fixtures.core import context, driver, sso_login_info, invalid_username, exporter_sso_login_info
from fixtures.urls import exporter_url, internal_url, sso_sign_in_url
from fixtures.register_organisation import register_organisation
from fixtures.apply_for_application import apply_for_standard_application, apply_for_clc_query, apply_for_standard_application_with_ueu

import helpers.helpers as utils
from pages.flags_pages import FlagsPages
from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.exporter_hub import ExporterHub
from pages.case_list_page import CaseListPage

# Screenshot in case of any test failure



def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = "{0}_{1}".format(class_name, exporter_url)
        #utils.save_screenshot(node.funcargs.get("driver"), name)


# Create driver and url command line adoption
def pytest_addoption(parser):
    env = str(os.environ.get('ENVIRONMENT'))
    if env == 'None':
        env = "dev"
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--exporter_url", action="store", default="https://exporter.lite.service." + env + ".uktrade.io/", help="url")
    parser.addoption("--internal_url", action="store", default="https://internal.lite.service." + env + ".uktrade.io/", help="url")
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")


@given('I go to exporter homepage')
def go_to_exporter_given(driver, exporter_url):
    driver.get(exporter_url)


@when('I go to the internal homepage')
def when_go_to_internal_homepage(driver, internal_url):
    driver.get(internal_url)


@given('I go to internal homepage')
def go_to_internal_homepage(driver, internal_url, sso_sign_in_url, sso_login_info):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_login_info['email'])
    driver.find_element_by_name("password").send_keys(sso_login_info['password'])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@when('I go to internal homepage and sign in')
def go_to_internal_homepage_sign_in(driver, internal_url, sso_sign_in_url, sso_login_info):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_login_info['email'])
    driver.find_element_by_name("password").send_keys(sso_login_info['password'])
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@when('I go to exporter homepage')
def go_to_exporter_when(driver, exporter_url):
    driver.get(exporter_url)


@when('I login to exporter homepage')
def login_to_exporter(driver, exporter_url, exporter_sso_login_info, register_organisation):
    driver.get(exporter_url)
    exporter_hub = ExporterHub(driver)
    if "login" in driver.current_url:
        exporter_hub.login(exporter_sso_login_info['email'], exporter_sso_login_info['password'])


@when('I click on application previously created')
def click_on_created_application(driver, context):
    driver.find_element_by_css_selector('.lite-cases-table').find_element_by_xpath("//*[text()[contains(.,'" + context.app_id + "')]]").click()


@when('I click on application previously created with pre incorporated goods')
def click_on_created_application_with_ueu(driver, apply_for_standard_application_with_ueu, context):
    driver.find_element_by_css_selector('.lite-cases-table').find_element_by_xpath("//*[text()[contains(.,'" + context.app_id + "')]]").click()


@given('I create application or application has been previously created')
def create_app(driver, register_organisation, apply_for_standard_application):
    pass


@given('I create clc query or clc query has been previously created')
def create_clc(driver, register_organisation, apply_for_clc_query):
    pass



@when('I click submit button')
def click_on_submit_button(driver):
    shared = Shared(driver)
    shared.click_submit()


@then(parsers.parse('I see error message "{expected_error}"'))
def error_message_shared(driver, expected_error):
    shared = Shared(driver)
    assert expected_error in shared.get_text_of_error_message(), "expected error message is not displayed"


@when('I click sites link')
def i_click_sites_link(driver):
    exporter = ExporterHub(driver)
    exporter.click_sites_link()


@when('I click new site')
def click_new_site(driver):
    exporter = ExporterHub(driver)
    exporter.click_new_sites_link()


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
def assert_case_is_present(driver, register_organisation, apply_for_clc_query, context):
    case_list_page = CaseListPage(driver)
    assert case_list_page.assert_case_is_present(context.case_id), "clc case ID is not present on page"


@when('I click on the clc-case previously created')
def click_on_clc_case_previously_created(driver, context):
    case_list_page = CaseListPage(driver)
    assert case_list_page.assert_case_is_present(context.case_id)
    driver.find_element_by_css_selector('.lite-cases-table').find_element_by_xpath("//*[text()[contains(.,'" + context.case_id + "')]]").click()
