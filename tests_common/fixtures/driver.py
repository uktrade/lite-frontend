import base64

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from _pytest.fixtures import fixture


@fixture(scope="session", autouse=True)
def driver(request, api_client, environment):
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
