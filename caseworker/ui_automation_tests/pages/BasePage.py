from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ui_automation_tests.shared import functions


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        # Wait for the cases list to load before interacting with the page
        if functions.element_with_id_exists(self.driver, "link-queue"):
            WebDriverWait(driver, 10).until(
                expected_conditions.visibility_of_element_located((By.ID, "text-case-count"))
            )

        # The case header is sticky and can often overlay elements preventing clicks,
        # therefore disable the stickyness of the header when running tests
        if functions.element_with_id_exists(self.driver, "app-header"):
            self.driver.execute_script("document.getElementById('app-header').style.position = 'relative';")
