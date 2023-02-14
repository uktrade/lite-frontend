from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from ui_tests.caseworker.pages.BasePage import BasePage


class AddEditFlagPage(BasePage):

    INPUT_NAME_ID = "name"
    SELECT_LEVEL_ID = "level"
    RADIOBUTTTON_COLOUR_ID_PREFIX = "colour-"
    INPUT_LABEL_ID = "label"
    INPUT_PRIORITY_ID = "priority"
    INPUT_BLOCKING_APPROVAL_PARTIAL_ID = "blocks_finalising-"

    def enter_name(self, name):
        self.driver.find_element(by=By.ID, value=self.INPUT_NAME_ID).clear()
        self.driver.find_element(by=By.ID, value=self.INPUT_NAME_ID).send_keys(name)

    def select_level(self, level):
        Select(self.driver.find_element(by=By.ID, value=self.SELECT_LEVEL_ID)).select_by_visible_text(level)

    def select_colour(self, colour):
        self.driver.find_element(by=By.ID, value=self.RADIOBUTTTON_COLOUR_ID_PREFIX + colour).click()

    def enter_label(self, label):
        self.driver.find_element(by=By.ID, value=self.INPUT_LABEL_ID).clear()
        self.driver.find_element(by=By.ID, value=self.INPUT_LABEL_ID).send_keys(label)

    def enter_priority(self, priority: int):
        self.driver.find_element(by=By.ID, value=self.INPUT_PRIORITY_ID).clear()
        self.driver.find_element(by=By.ID, value=self.INPUT_PRIORITY_ID).send_keys(priority)

    def enter_blocking_approval(self, blocks_finalising: str):
        self.driver.find_element(by=By.ID, value=self.INPUT_BLOCKING_APPROVAL_PARTIAL_ID + blocks_finalising).click()
