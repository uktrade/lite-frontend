import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from _pytest.fixtures import fixture

from ..fixtures.cci import enable_browser_stack


@fixture(scope="session", autouse=True)
def driver(request, api_client):
    is_headless = request.config.getoption("--headless")

    chrome_options = webdriver.ChromeOptions()
    if is_headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {"download.default_directory": "/tmp"}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.implicitly_wait(20)
    driver.get("about:blank")
    driver.maximize_window()

    yield driver

    driver.close()
    driver.quit()
