import os
from selenium import webdriver
from http import HTTPStatus


class Logging:
    @staticmethod
    def debug(debug_str):
        print(debug_str)


logging = Logging()
ENVIRONMENT = os.environ.get("ENVIRONMENT")
BROWSER_HOSTS = os.environ.get("BROWSER_HOSTS")
TEST_HOSTS = os.environ.get("BROWSER_HOSTS")
AUTH_USER_NAME = os.environ.get("AUTH_USER_NAME")
AUTH_USER_PASSWORD = os.environ.get("AUTH_USER_PASSWORD")
ENDPOINT = os.environ.get("ENDPOINT")
BROWSER_STACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME")
BROWSER_STACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")


class wait_for_page_load_after_action(object):
    def __init__(self, driver, *, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    def __enter__(self):
        self.old_page = self.driver.find_element_by_tag_name("html")

    def __exit__(self, *_):
        self.wait_for(self.page_has_loaded)

    def page_has_loaded(self):
        new_page = self.driver.find_element_by_tag_name("html")
        has_loaded = new_page.id != self.old_page.id
        if has_loaded:
            logging.debug(f"Page has loaded. {self.driver.current_url}")
        else:
            logging.debug(f"Waiting for {self.driver.current_url} page to load...")
        return has_loaded

    def wait_for(self, condition_function):
        import time

        start_time = time.time()
        while time.time() < start_time + self.timeout:
            if condition_function():
                return True
            else:
                time.sleep(0.2)
        raise Exception(f"Timed out after {self.timeout}s of waiting for the new page to load")


def create_browserstack_driver(bs_username, bs_access_key):
    desired_cap = {
        "browser": "Chrome",
        "browser_version": "80.0",
        "os": "OS X",
        "os_version": "High Sierra",
        "resolution": "1920x1080",
        "name": "LITE-POC exporter login on chrome test",
        "build": "CircleCI e2e exporter tests",
        "project": "CCI-BS-POC",
    }

    return webdriver.Remote(
        command_executor=f"https://{bs_username}:{bs_access_key}@hub-cloud.browserstack.com/wd/hub",
        desired_capabilities=desired_cap,
    )


def enable_browser_stack(request, api_test_client):
    client = api_test_client["the_client"]

    test_hosts = list(TEST_HOSTS.replace("${ENVIRONMENT}", ENVIRONMENT).split(","))
    for host in test_hosts:
        logging.debug(f"Allowing test runner access to {host}")
        client.auth_basic(AUTH_USER_NAME, AUTH_USER_PASSWORD)
        response = client.session.request("GET", f"https://{host}{ENDPOINT}")
        assert response.status_code == HTTPStatus.OK
        assert response.text == "ok"

    driver = create_browserstack_driver(BROWSER_STACK_USERNAME, BROWSER_STACK_ACCESS_KEY)

    def timeout_shim(self, time=0):
        logging.debug(f"WARNING: set_timeout_to({time}) called and will do nothing")

    driver.set_timeout_to = timeout_shim

    browser_hosts = list(BROWSER_HOSTS.replace("${ENVIRONMENT}", ENVIRONMENT).split(","))
    for host in browser_hosts:
        logging.debug(f"Allowing browser access to {host}")
        url = f"https://{AUTH_USER_NAME}:{AUTH_USER_PASSWORD}@{host}{ENDPOINT}"
        with wait_for_page_load_after_action(driver):
            driver.get(url)
            assert "Access Denied" not in driver.page_source

    def fin():
        driver.close()
        driver.quit()

    request.addfinalizer(fin)
    return driver
