from conf.settings import env
import os
import types
from selenium import webdriver
from pytest import fixture


def timeout_off(self):
    self.implicitly_wait(0)


def timeout_on(self):
    self.implicitly_wait(10)

# Create driver fixture that initiates chrome
@fixture(scope="session", autouse=True)
def driver(request):
    browser = request.config.getoption("--driver")

    chrome_options = webdriver.ChromeOptions()
    if str(os.environ.get('TEST_TYPE_HEADLESS')) == 'True':
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')

    if browser == 'chrome':
        if str(os.environ.get('ENVIRONMENT')) == 'None':
            browser = webdriver.Chrome("chromedriver", chrome_options=chrome_options)
        else:
            browser = webdriver.Chrome(chrome_options=chrome_options)

        browser.timeout_off = types.MethodType(timeout_off, browser)
        browser.timeout_on = types.MethodType(timeout_on, browser)
        browser.get("about:blank")
        browser.timeout_on()
        return browser
    else:
        print('Only Chrome is supported at the moment')

    def fin():
        driver.quit()
    request.addfinalizer(fin)


@fixture(scope="session")
def context(request):
    class Context(object):
        pass

    return Context()


@fixture(scope="session")
def sso_login_info(request):
    sso_email = env('TEST_SSO_EMAIL')
    sso_password = env('TEST_SSO_PASSWORD')

    return {'email': sso_email, 'password': sso_password}


@fixture(scope="session")
def exporter_sso_login_info(request):
    exporter_sso_email = env('TEST_EXPORTER_SSO_EMAIL')
    exporter_sso_password = env('TEST_EXPORTER_SSO_PASSWORD')

    return {'email': exporter_sso_email, 'password': exporter_sso_password}


@fixture(scope="module")
def invalid_username(request):
    return "invalid@mail.com"
