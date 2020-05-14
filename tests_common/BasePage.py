from selenium.webdriver.remote.webdriver import WebDriver

from shared import functions


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        # The case header is sticky and can often overlay elements preventing clicks,
        # therefore disable the stickyness of the header when running tests
        if functions.element_with_id_exists(self.driver, "app-header"):
            self.driver.execute_script("document.getElementById('app-header').style.position = 'relative';")
