from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

from _pytest.fixtures import fixture


@fixture(scope="session", autouse=True)
def driver(request, api_client, environment, tmp_download_path):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")

    # This path is shared between different containers with different users and
    # permissions.
    # We are allowing anyone to read and write to this to handle this mix.
    tmp_download_path.chmod(0o777)
    prefs = {"download.default_directory": str(tmp_download_path)}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_binary_location = request.config.getoption("--chrome-binary-location")
    if chrome_binary_location:
        chrome_options.binary_location = chrome_binary_location

    is_headless = request.config.getoption("--headless")
    if is_headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Remote(
            command_executor="http://selenium-hub:4444/wd/hub",
            options=chrome_options,
        )
    driver.implicitly_wait(20)
    driver.get("about:blank")
    driver.maximize_window()

    yield driver

    driver.close()
    driver.quit()
