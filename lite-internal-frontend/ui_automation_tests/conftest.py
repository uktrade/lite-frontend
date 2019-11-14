import os

from pytest_bdd import given, when, then, parsers
from selenium.common.exceptions import NoSuchElementException

from pages.organisation_page import OrganisationPage

from ui_automation_tests.fixtures.env import environment  # noqa
from ui_automation_tests.fixtures.add_a_flag import add_uae_flag, add_suspicious_flag, add_organisation_suspicious_flag, add_new_flag  # noqa
from ui_automation_tests.fixtures.add_queue import add_queue  # noqa
from ui_automation_tests.fixtures.add_a_team import add_a_team  # noqa
from ui_automation_tests.fixtures.add_a_document_template import add_a_document_template, get_template_id  # noqa
from ui_automation_tests.fixtures.add_a_picklist import add_a_letter_paragraph_picklist, add_an_ecju_query_picklist, add_a_proviso_picklist, add_a_standard_advice_picklist, add_a_report_summary_picklist  # noqa
from ui_automation_tests.shared.fixtures.apply_for_application import apply_for_standard_application, apply_for_clc_query, apply_for_eua_query, apply_for_open_application  # noqa
from ui_automation_tests.shared.fixtures.driver import driver  # noqa
from ui_automation_tests.shared.fixtures.sso_sign_in import sso_sign_in  # noqa
from ui_automation_tests.shared.fixtures.core import context, invalid_username, seed_data_config, exporter_info, internal_info  # noqa
from ui_automation_tests.shared.fixtures.urls import internal_url, sso_sign_in_url, api_url  # noqa

import shared.tools.helpers as utils
from pages.assign_flags_to_case import CaseFlagsPages

from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.case_list_page import CaseListPage
from pages.application_page import ApplicationPage
from pages.queues_pages import QueuesPages


def pytest_addoption(parser):
    env = str(os.environ.get('ENVIRONMENT'))
    if env == 'None':
        env = 'dev'

    parser.addoption('--driver', action='store', default='chrome', help='Type in browser type')
    parser.addoption('--sso_sign_in_url', action='store', default='https://sso.trade.uat.uktrade.io/login/', help='url')

    if env.lower() == 'local':
        parser.addoption('--internal_url', action='store', default='http://localhost:' + str(os.environ.get('PORT')), help='url')

        # Get LITE API URL.
        lite_api_url = os.environ.get(
            'LOCAL_LITE_API_URL',
            os.environ.get('LITE_API_URL'),
        )
        parser.addoption(
            '--lite_api_url',
            action='store',
            default=lite_api_url,
            help='url',
        )

    elif env == 'demo':
        raise NotImplementedError('This is the demo environment - Try another environment instead')
    else:
        parser.addoption('--internal_url', action='store',
                         default='https://internal.lite.service.' + env + '.uktrade.io/', help='url')
        parser.addoption('--lite_api_url', action='store',
                         default='https://lite-api-' + env + '.london.cloudapps.digital/', help='url')


# Create driver and url command line adoption
def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace('.py::', '_class_')
        name = ' {0}_{1}'.format(class_name, 'error')
        try:
            utils.save_screenshot(node.funcargs.get('driver'), name)
        except Exception:  # noqa
            pass


@when('I go to the internal homepage')  # noqa
def when_go_to_internal_homepage(driver, internal_url):
    driver.get(internal_url)


@given('I go to internal homepage')  # noqa
def go_to_internal_homepage(driver, internal_url, sso_sign_in):
    driver.get(internal_url)


@given('I sign in to SSO or am signed into SSO')  # noqa
def sign_into_sso(driver, sso_sign_in):
    pass


@when('I go to application previously created')  # noqa
def click_on_created_application(driver, context, internal_url):
    driver.get(internal_url.rstrip('/') + '/cases/' + context.case_id)


@when('I go to open application previously created')  # noqa
def click_on_created_application(driver, context, internal_url):
    driver.get(internal_url.rstrip('/') + '/cases/' + context.case_id)


@when('I go to end user advisory previously created')  # noqa
def click_on_created_eua(driver, context):
    driver.find_element_by_link_text(context.eua_id).click()


@when('I go to clc query previously created')  # noqa
def click_on_created_application(driver, context, internal_url):
    driver.get(internal_url.rstrip('/') + '/cases/' + context.clc_case_id)


@given('I create application or application has been previously created')  # noqa
def create_app(driver, apply_for_standard_application):
    pass


@given('I create open application or open application has been previously created')  # noqa
def create_open_app(driver, apply_for_open_application):
    pass


@given('I create clc query or clc query has been previously created')  # noqa
def create_clc(driver, apply_for_clc_query):
    pass


@given('I create eua query or eua query has been previously created')  # noqa
def create_eua(driver, apply_for_eua_query):
    pass


@then(parsers.parse('I see error message "{expected_error}"'))  # noqa
def error_message_shared(driver, expected_error):
    shared = Shared(driver)
    assert expected_error in shared.get_text_of_error_message(0), 'expected error message is not displayed'


@when('I click continue')  # noqa
def i_click_continue(driver):
    Shared(driver).click_submit()


@when('I click back')  # noqa
def i_click_back(driver):
    Shared(driver).click_back()


@given('I go to flags')  # noqa
def go_to_flags(driver, internal_url, sso_sign_in):
    driver.get(internal_url.rstrip('/')+'/flags')


@when('I go to flags via menu')  # noqa
def go_to_flags_menu(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_flags()


@when('I go to users')  # noqa
def go_to_users(driver):
    header = HeaderPage(driver)
    header.open_users()


@when('I create a clc_query')  # noqa
def create_clc_query(driver, apply_for_clc_query, context):
    pass


@when('I click on the clc-case previously created')  # noqa
def click_on_clc_case_previously_created(driver, context):
    case_list_page = CaseListPage(driver)
    assert case_list_page.assert_case_is_present(context.case_id)
    case_list_page.click_on_href_within_cases_table(context.case_id)


@when('I click progress application')  # noqa
def click_post_note(driver):
    application_page = ApplicationPage(driver)
    application_page.click_progress_application()


@when(parsers.parse('I select status "{status}" and save'))  # noqa
def select_status_save(driver, status, context):
    application_page = ApplicationPage(driver)
    application_page.select_status(status)
    context.status = status
    context.date_time_of_update = utils.get_formatted_date_time_h_m_pm_d_m_y()
    Shared(driver).click_submit()


@when('I click on new queue in dropdown')  # noqa
def new_queue_shown_in_dropdown(driver, context):
    CaseListPage(driver).click_on_queue_name(context.queue_name)


@then('there are no cases shown')  # noqa
def no_cases_shown(driver):
    assert 'There are no new cases to show.' in QueuesPages(driver).get_no_cases_text(),\
        'There are cases shown in the newly created queue.'


@when(parsers.parse('I click on the "{queue_name}" queue in dropdown'))  # noqa
def system_queue_shown_in_dropdown(driver, queue_name):
    CaseListPage(driver).click_on_queue_name(queue_name)


@when(parsers.parse('I click on the added queue in dropdown'))  # noqa
def system_queue_shown_in_dropdown(driver, context):
    CaseListPage(driver).click_on_queue_name(context.queue_name)


@when('I enter in queue name Review')  # noqa
def add_a_queue(driver, context, add_queue):
    pass


@when('I go to queues via menu')  # noqa
def go_to_queues_via_menu(driver):
    HeaderPage(driver).click_lite_menu()
    HeaderPage(driver).click_queues()


@given('I go to queues')  # noqa
def go_to_queues(driver, sso_sign_in, internal_url):
    driver.get(internal_url.rstrip('/') + '/queues/')


@when('I add case to newly created queue')  # noqa
def move_case_to_new_queue(driver, context):
    ApplicationPage(driver).click_move_case_button()
    if not driver.find_element_by_id(context.queue_name).is_selected():
        driver.find_element_by_id(context.queue_name).click()
    Shared(driver).click_submit()


@when('I select previously created flag')  # noqa
def assign_flags_to_case(driver, context):
    case_flags_pages = CaseFlagsPages(driver)
    case_flags_pages.select_flag(context, context.flag_name)
    shared = Shared(driver)
    shared.click_submit()


@given('I create report summary picklist') # noqa
def add_report_summary_picklist(add_a_report_summary_picklist):
    pass


@then('I see the added flags on the queue')  # noqa
def added_flags_on_queue(driver, context):
    elements = Shared(driver).get_rows_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.case_id, complete_match=False)
    driver.set_timeout_to(0)
    try:
        if elements[no].find_element_by_id('chevron').is_displayed():
            element = elements[no].find_element_by_css_selector('.lite-accordian-table__chevron')
            element.click()
    except NoSuchElementException:
        pass
    driver.set_timeout_to(10)
    assert context.flag_name in elements[no].text


@then('I see previously created application')  # noqa
def see_queue_in_queue_list(driver, context):
    assert QueuesPages(driver).is_case_on_the_list(context.case_id) == 1, 'previously created application is not displayed ' + context.case_id


@when('I add a flag called Suspicious at level Organisation')  # noqa
def add_a_suspicious_flag(driver, add_organisation_suspicious_flag):
    pass


@when('I go to the organisation which submitted the case') # noqa
def go_to_the_organisation_which_submitted_the_case(driver):
    ApplicationPage(driver).go_to_organisation()


@when('I click the edit flags link')  # noqa
def go_to_edit_flags(driver):
    OrganisationPage(driver).click_edit_organisation_flags()


@then('the previously created organisations flag is assigned')  # noqa
def assert_flag_is_assigned(driver, context):
    assert OrganisationPage(driver).is_organisation_flag_applied(context.flag_name)


@when('I click chevron')  # noqa
def click_chevron(driver, context):
    elements = Shared(driver).get_rows_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.case_id, complete_match=False)
    try:
        if elements[no].find_element_by_id('chevron').is_displayed():
            element = elements[no].find_element_by_css_selector('.lite-accordian-table__chevron')
            element.click()
    except NoSuchElementException:
        pass
    driver.set_timeout_to(10)
