import os
import types

from _pytest.fixtures import fixture
from selenium import webdriver

from ..tools.utils import set_timeout_to, set_timeout_to_10_seconds

# Create driver fixture that initiates chrome
@fixture(scope="session", autouse=True)
def driver(request):
    browser = request.config.getoption("--driver")

    chrome_options = webdriver.ChromeOptions()
    if str(os.environ.get("TEST_TYPE_HEADLESS")) == "True":
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    # Use proxy settings provided in config file for security testing
    if os.environ.get("PROXY_IP_PORT") is not None:
        chrome_options.add_argument(
            "--proxy-server=%s" % str(os.environ.get("PROXY_IP_PORT"))
        )

    if browser == "chrome":
        if str(os.environ.get("ENVIRONMENT")) == "None":
            browser = webdriver.Chrome("chromedriver", chrome_options=chrome_options)
        else:
            browser = webdriver.Chrome(chrome_options=chrome_options)

        browser.set_timeout_to = types.MethodType(set_timeout_to, browser)
        browser.set_timeout_to_10_seconds = types.MethodType(
            set_timeout_to_10_seconds, browser
        )
        browser.get("about:blank")
        browser.set_timeout_to_10_seconds()
        return browser
    else:
        print("Only Chrome is supported at the moment")

    def fin():
        driver.quit()

    request.addfinalizer(fin)
