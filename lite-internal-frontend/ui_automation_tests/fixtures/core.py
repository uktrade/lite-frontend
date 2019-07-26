from conf.settings import env
import os
from selenium import webdriver
from pytest import fixture


# Create driver fixture that initiates chrome
@fixture(scope="session", autouse=True)
def driver(request):
    browser = request.config.getoption("--driver")

    chrome_options = webdriver.ChromeOptions()
    # remove this line to see it running in browser.
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')

    if browser == 'chrome':
        if str(os.environ.get('ENVIRONMENT')) == 'None':
            browser = webdriver.Chrome("chromedriver", chrome_options=chrome_options)
        else:
            browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get("about:blank")
        browser.implicitly_wait(10)
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
