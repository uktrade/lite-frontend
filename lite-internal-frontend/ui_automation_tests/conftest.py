import os
import pytest
from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from selenium import webdriver
import helpers.helpers as utils
from conf.settings import env
from pages.exporter_hub import ExporterHub
from pages.header_page import HeaderPage
from pages.flags_pages import FlagsPages
from pages.shared import Shared

# Screenshot in case of any test failure


def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = "{0}_{1}".format(class_name, exporter_url)
        # utils.save_screenshot(node.funcargs.get("driver"), name)


# Create driver and url command line adoption
def pytest_addoption(parser):
    env = str(os.environ.get('ENVIRONMENT'))
    if env == 'None':
        env = "dev"
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--exporter_url", action="store",
                     default="https://exporter.lite.service." + env + ".uktrade.io/", help="url")
    parser.addoption("--internal_url", action="store",
                     default="https://internal.lite.service." + env + ".uktrade.io/", help="url")
    # parser.addoption("--exporter_url", action="store", default="http://localhost:9000", help="url")
    # parser.addoption("--internal_url", action="store", default="http://localhost:8080", help="url")
    # parser.addoption("--exporter_url", action="store", default="http://localhost:8300", help="url")
    # parser.addoption("--internal_url", action="store", default="http://localhost:8200", help="url")
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")


# Create driver fixture that initiates chrome
@pytest.fixture(scope="module", autouse=True)
def driver(request):
    browser = request.config.getoption("--driver")
    if browser == 'chrome':
        if str(os.environ.get('ENVIRONMENT')) == 'None':
            browser = webdriver.Chrome("chromedriver")
        else:
            browser = webdriver.Chrome()
        browser.get("about:blank")
        browser.implicitly_wait(3)
        return browser
    else:
        print('only chrome is supported at the moment')

    def fin():
        driver.quit()
        request.addfinalizer(fin)


@pytest.fixture
def context():
    class Context(object):
        pass

    return Context()


# Create url fixture
@pytest.fixture(scope="module")
def exporter_url(request):
    return request.config.getoption("--exporter_url")


@pytest.fixture(scope="module")
def internal_url(request):
    return request.config.getoption("--internal_url")


@pytest.fixture
def test_teardown(driver):
    driver.quit()


@pytest.fixture(scope="module")
def sso_sign_in_url(request):
    return request.config.getoption("--sso_sign_in_url")


@pytest.fixture(scope="module")
def invalid_username():
    return "invalid@mail.com"


sso_email = env('TEST_SSO_EMAIL')
sso_password = env('TEST_SSO_PASSWORD')


@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url, sso_sign_in_url):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@when('I go to the internal homepage')
def when_go_to_internal_homepage(driver, internal_url):
    driver.get(internal_url)


@given('I go to internal homepage')
def go_to_internal_homepage(driver, internal_url, sso_sign_in_url):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@when('I go to internal homepage and sign in')
def go_to_internal_homepage_sign_in(driver, internal_url, sso_sign_in_url):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@when('I go to exporter homepage')
def go_to_exporter_when(driver, exporter_url):
    driver.get(exporter_url)


@when(parsers.parse('I login to exporter homepage with username "{username}" and "{password}"'))
def login_to_exporter(driver, username, password):
    if username == "TestBusinessForSites@mail.com":
        username = context.email
    exporter_hub = ExporterHub(driver)
    if "login" in driver.current_url:
        exporter_hub.login(username, password)


@when('I click on application previously created')
def click_on_created_application(driver):
    driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_id + "')]]").click()


@when('I click on an application previously created')
def click_on_a_created_application(driver):
    driver.find_element_by_css_selector(".lite-cases-table a[href*='/cases/']").click()


@when('I click submit button')
def click_on_submit_button(driver):
    shared = Shared(driver)
    shared.click_submit()


@then(parsers.parse('I see error message "{expected_error}"'))
def error_message_shared(driver, expected_error):
    shared = Shared(driver)
    assert expected_error in shared.get_text_of_error_message()


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
def add_a_flag(driver, flag_name, flag_level):
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
