import os
import types

from selenium import webdriver
from _pytest.fixtures import fixture
from ..fixtures.cci import enable_browser_stack
from ..tools.utils import set_timeout_to_10_seconds, set_timeout_to


@fixture(scope="session", autouse=True)
def driver(request, api_client_config):
    if os.getenv("TEST_TYPE_BROWSER_STACK", "False") == "True":
        driver = enable_browser_stack(request, api_client_config)
        return driver

    browser = request.config.getoption("--driver")

    chrome_options = webdriver.ChromeOptions()
    if str(os.environ.get("TEST_TYPE_HEADLESS")) == "True":
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    # Use proxy settings provided in config file for security testing
    if os.environ.get("PROXY_IP_PORT") is not None:
        chrome_options.add_argument("--proxy-server=%s" % str(os.environ.get("PROXY_IP_PORT")))

    if browser == "chrome":
        return create_selenium_chrome_driver(chrome_options, request)
    else:
        print("Only Chrome is supported at the moment")


def create_selenium_chrome_driver(chrome_options, request):
    if str(os.environ.get("ENVIRONMENT")) == "None":
        driver = webdriver.Chrome("chromedriver", options=chrome_options)  # noqa
    else:
        driver = webdriver.Chrome(options=chrome_options)  # noqa
    driver.set_timeout_to = types.MethodType(set_timeout_to, driver)
    driver.set_timeout_to_10_seconds = types.MethodType(set_timeout_to_10_seconds, driver)
    driver.get("about:blank")
    driver.set_timeout_to(10)

    def fin():
        driver.quit()

    request.addfinalizer(fin)
    return driver
