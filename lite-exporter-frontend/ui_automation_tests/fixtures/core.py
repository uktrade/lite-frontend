from conf.settings import env
import os
import types
from selenium import webdriver
from pytest import fixture


def set_timout_to(self, num=0):
    self.implicitly_wait(num)


def set_timeout_to_10(self):
    self.implicitly_wait(10)


# Create driver fixture that initiates chrome
@fixture(scope="session", autouse=True)
def driver(request):
    browser = request.config.getoption("--driver")

    chrome_options = webdriver.ChromeOptions()
    # remove this line to see it running in browser.
    if str(os.environ.get('TEST_TYPE_HEADLESS')) == 'True':
        chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')

    # Use proxy settings provided in config file for security testing
    if os.environ.get('PROXY_IP_PORT') is not None:
        chrome_options.add_argument('--proxy-server=%s' % str(os.environ.get('PROXY_IP_PORT')))

    if browser == 'chrome':
        if str(os.environ.get('ENVIRONMENT')) == 'None':
            browser = webdriver.Chrome("chromedriver", options=chrome_options)
        else:
            browser = webdriver.Chrome(options=chrome_options)
        browser.get("about:blank")
        browser.set_timeout_to = types.MethodType(set_timout_to, browser)
        browser.set_timeout_to_10 = types.MethodType(set_timeout_to_10, browser)
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
def exporter_sso_login_info(request):
    exporter_sso_email = env('TEST_EXPORTER_SSO_EMAIL')
    exporter_sso_password = env('TEST_EXPORTER_SSO_PASSWORD')

    return {'email': exporter_sso_email, 'password': exporter_sso_password}


@fixture(scope="session")
def s3_key(request):
    s3_key = env('TEST_S3_KEY')
    return s3_key


@fixture(scope="session")
def invalid_username(request):
    return "invalid@mail.com"


@fixture(scope="session")
def seed_data_config(request, exporter_sso_login_info, s3_key):
    exporter_sso_email = exporter_sso_login_info['email']
    api_url = request.config.getoption("--lite_api_url")
    return {'api_url': api_url, 'email': exporter_sso_email, 's3_key': s3_key}
