import base64

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from _pytest.fixtures import fixture


@fixture(scope="session", autouse=True)
def driver(request, api_client, environment):
    is_headless = request.config.getoption("--headless")

    chrome_options = webdriver.ChromeOptions()
    # if is_headless:
    #     chrome_options.add_argument("--headless")
    #     chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {"download.default_directory": "/tmp"}
    chrome_options.add_experimental_option("prefs", prefs)

    desired_capabilities = DesiredCapabilities.CHROME.copy()
    desired_capabilities["acceptInsecureCerts"] = True

    driver = webdriver.Remote(
        command_executor="http://host.docker.internal:4444/wd/hub",
        options=chrome_options,
        desired_capabilities=desired_capabilities,
    )
    driver.implicitly_wait(20)
    driver.get("about:blank")
    driver.maximize_window()

    if environment("BASIC_AUTH_ENABLED", default="False") == "True":
        auth = (
            base64.encodebytes(f"{environment('AUTH_USER_NAME')}:{environment('AUTH_USER_PASSWORD')}".encode())
            .decode()
            .strip()
        )

        def interceptor(req):
            if req.host.endswith("uktrade.digital"):
                req.headers["Authorization"] = f"Basic {auth}"

        driver.request_interceptor = interceptor

    yield driver

    driver.close()
    driver.quit()
