import pytest
from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from selenium import webdriver
import os

# Screenshot in case of any test failure
def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = "{0}_{1}".format(class_name, exporter_url)
        # utils.save_screenshot(node.funcargs.get("driver"), name)


# Create driver and url command line addoption
def pytest_addoption(parser):
    env = str(os.environ.get('ENVIRONMENT'))
    if env == 'None':
        env = "dev"
    print("touched: " + env)
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    # parser.addoption("--exporter_url", action="store", default="https://lite-exporter-frontend-" + env + ".london.cloudapps.digital/", help="url")
    parser.addoption("--exporter_url", action="store",
                     default="https://exporter.lite.service." + env + ".uktrade.io/", help="url")
    # parser.addoption("--internal_url", action="store", default="https://lite-internal-frontend-" + env + ".london.cloudapps.digital/", help="url")
    parser.addoption("--internal_url", action="store",
                     default="https://internal.lite.service." + env + ".uktrade.io/", help="url")
    #parser.addoption("--exporter_url", action="store", default="http://localhost:9000", help="url")
    #parser.addoption("--internal_url", action="store", default="http://localhost:8080", help="url")
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


# Create url fixture
@pytest.fixture(scope="module")
def exporter_url(request):
    return request.config.getoption("--exporter_url")

@pytest.fixture(scope="module")
def internal_url(request):
    return request.config.getoption("--internal_url")

# @pytest.fixture(scope="module")
# def sign_in_url(request):
#     return request.config.getoption("--sso_sign_in_url")

@pytest.fixture(scope="module")
def invalid_username():
    return "invalid@mail.com"

@pytest.fixture(scope="module")
def internal_login_url():
    return "https://sso.trade.uat.uktrade.io/login/"

@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url, sign_in_url):
    driver.get(sign_in_url)
    driver.find_element_by_name("username").send_keys("test-uat-user@digital.trade.gov.uk")
    driver.find_element_by_name("password").send_keys("5cCIlffSrqszgOuw23VEOECnM")
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


# applying for licence
# there might be some redundant code below


@given('I go to internal homepage')
def go_to_internal_homepage(driver, internal_url, internal_login_url):
    driver.get(internal_login_url)
    driver.find_element_by_name("username").send_keys("test-uat-user@digital.trade.gov.uk")
    driver.find_element_by_name("password").send_keys("5cCIlffSrqszgOuw23VEOECnM")
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@given('I go to exporter homepage')
def go_to_exporter(driver, exporter_url):
    driver.get(exporter_url)


@when('I go to exporter homepage')
def go_to_exporter_when(driver, exporter_url):
    driver.get(exporter_url)


@when(parsers.parse('I login to exporter homepage with username "{username}" and "{password}"'))
def login_to_exporter(driver, username, password):
    exporter_hub = ExporterHubPage(driver)
    if "login" in driver.current_url:
        exporter_hub.login(username, password)


@when(parsers.parse('I login to exporter homepage with context after edit'))
def login_to_exporter(driver, password):
    exporter_hub = ExporterHubPage(driver)
    if "login" in driver.current_url:
        exporter_hub.login(context.edited_email, password)


# utils
@then(parsers.parse('driver title equals "{expected_text}"'))
def assert_title_text(driver, expected_text):
    assert driver.title == expected_text


@when('I click on apply for a license button')
def click_apply_licence(driver):
    exporter = ExporterHubPage(driver)
    exporter.click_apply_for_a_licence()


@when('I click on start button')
def click_start_button(driver):
    apply = ApplyForALicencePage(driver)
    apply.click_start_now_btn()


@when('I enter in name for application and continue')
def enter_application_name(driver):
    apply = ApplyForALicencePage(driver)
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id
    app_name = "Test Application " + app_time_id
    apply.enter_name_or_reference_for_application(app_name)
    context.app_id = app_name
    apply.click_save_and_continue()


@when(parsers.parse('I select "{type}" application and continue'))
def enter_type_of_application(driver, type):
    context.type = type
    # type needs to be standard or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence(type)
    apply.click_continue()


@when(parsers.parse('I select "{permanent_or_temporary}" option and continue'))
def enter_permanent_or_temporary(driver, permanent_or_temporary):
    context.perm_or_temp = permanent_or_temporary
    # type needs to be standard or temporary
    apply = ApplyForALicencePage(driver)
    apply.click_permanent_or_temporary_button(permanent_or_temporary)
    apply.click_continue()


@when(parsers.parse(
    'I select "{yes_or_no}" for whether I have an export licence and "{reference}" if I have a reference and continue'))
def enter_export_licence(driver, yes_or_no, reference):
    apply = ApplyForALicencePage(driver)
    apply.click_export_licence_yes_or_no(yes_or_no)
    context.ref = reference
    apply.type_into_reference_number(reference)
    apply.click_continue()


@when('I click sites link')
def i_click_sites_link(driver):
    app = ApplicationOverviewPage(driver)
    app.click_sites_link()


@when('I click continue')
def i_click_continue(driver):
    driver.find_element_by_css_selector("button[type*='submit']").click()


@then(parsers.parse('error message is "{expected_error}"'))
def error_message_is(driver, expected_error):
    shared = Shared(driver)
    assert shared.is_error_message_displayed()
    assert expected_error in shared.get_text_of_error_message()


@when(parsers.parse('I select the site at position "{no}"'))
def select_the_site_at_position(driver, no):
    sites = SitesPage(driver)
    sites.click_sites_checkbox(int(no) - 1)


@when('I click on goods link')
def click_my_goods_link(driver):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_my_goods()


@when('I click the add from organisations goods button')
def click_add_from_organisation_button(driver):
    driver.find_element_by_css_selector('a.govuk-button[href*="add_preexisting"]').click()


@when(parsers.parse(
    'I add a good with description "{description}" controlled "{controlled}" control code "{controlcode}" incorporated "{incorporated}" and part number "{part}"'))
def add_new_good(driver, description, controlled, controlcode, incorporated, part):
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    good_description = description + str(random.randint(1, 1000))
    good_part = part + str(random.randint(1, 1000))
    context.good_description = good_description
    context.part = good_part
    context.controlcode = controlcode
    add_goods_page.click_add_a_good()
    add_goods_page.enter_description_of_goods(good_description)
    add_goods_page.select_is_your_good_controlled(controlled)
    add_goods_page.enter_control_code(controlcode)
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product(incorporated)
    add_goods_page.enter_part_number(good_part)
    exporter_hub.click_save_and_continue()

@when(parsers.parse('I add an end user of type: "{type}", name: "{name}", website: "{website}", address: "{address}" and country "{country}"'))
def add_new_end_user(driver, type, name, website, address, country):
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.select_type(type)
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_name(name)
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_website(website)
    add_end_user_pages.click_continue()
    add_end_user_pages.enter_address(address)
    add_end_user_pages.enter_country(country)
    add_end_user_pages.click_continue()


@when('I click on end user')
def i_click_on_end_user(driver):
    app = ApplicationOverviewPage(driver)
    app.click_end_user_link()