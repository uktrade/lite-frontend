import base64
import os

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from _pytest.fixtures import fixture


@fixture(scope="session", autouse=True)
def driver(request, api_client, environment, tmp_download_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # This path is shared between different containers with different users and
    # permissions.
    # We are allowing anyone to read and write to this to handle this mix.
    os.chmod(tmp_download_path, 0o777)
    prefs = {"download.default_directory": tmp_download_path}
    chrome_options.add_experimental_option("prefs", prefs)

    desired_capabilities = DesiredCapabilities.CHROME.copy()
    desired_capabilities["acceptInsecureCerts"] = True

    is_headless = request.config.getoption("--headless")
    if is_headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    else:
        driver = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub",
            options=chrome_options,
            desired_capabilities=desired_capabilities,
        )
    driver.implicitly_wait(20)
    driver.get("about:blank")
    driver.maximize_window()

    yield driver

    driver.close()
    driver.quit()
