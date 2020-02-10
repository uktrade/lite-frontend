from selenium.common.exceptions import NoSuchElementException

from shared import functions
from shared.BasePage import BasePage
from shared.functions import element_with_css_selector_exists, element_with_id_exists


class GenericApplicationTaskListPage(BasePage):

    LOCATION_LINK = "link-locations"
    OPEN_GOODS_LINK = "link-products"
    LINK_END_USER_ID = "link-end-user"
    LINK_CONSIGNEE_ID = "link-consignee"
    LINK_SUPPORTING_DOCUMENTS_ID = "link-supporting-documents"
    ULTIMATE_END_USER_LINK = "link-ultimate_end_users"  # ID
    GOODS_ON_APPLICATION = "[id^=good-on-application-row]"  # CSS
    GOV_TABLES = ".govuk-table__body"  # CSS
    DELETE_END_USER_DOCUMENT = "end_user_document_delete"  # ID
    ATTACH_END_USER_DOCUMENT = "end_user_attach_doc"  # ID
    LINK_COUNTRIES_MATRIX_ID = "link-countries-matrix"
    REMOVE_GOOD_LINK = "a[href*='good-on-application']"
    REMOVE_GOODS_TYPE_LINK = "a[href*='goods-types/remove']"
    REMOVE_END_USER_LINK = "a[href*='remove']"
    REMOVE_CONSIGNEE_LINK = "a[href*='remove']"
    REMOVE_THIRD_PARTY_LINK = "a[href*='remove']"
    REMOVE_ADDITIONAL_DOCUMENT_LINK = "document_delete"  # ID
    LITE_TASK_LIST_ITEMS = ".lite-task-list__items"
    DELETE_ADDITIONAL_DOC_CONFIRM_YES = "delete_document_confirmation-yes"  # ID

    def click_supporting_documents_link(self):
        self.driver.find_element_by_id(self.LINK_SUPPORTING_DOCUMENTS_ID).click()

    def find_remove_goods_type_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_GOODS_TYPE_LINK)
        except NoSuchElementException:
            return None

    def get_remove_good_link(self):
        return self.driver.find_element_by_css_selector(self.REMOVE_GOOD_LINK)

    def find_remove_end_user_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_END_USER_LINK)
        except NoSuchElementException:
            return None

    def does_remove_end_user_exist(self, driver):
        return element_with_css_selector_exists(driver, self.REMOVE_END_USER_LINK)

    def find_remove_consignee_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_CONSIGNEE_LINK)
        except NoSuchElementException:
            return None

    def does_remove_consignee_exist(self, driver):
        return element_with_css_selector_exists(driver, self.REMOVE_CONSIGNEE_LINK)

    def find_remove_third_party_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_THIRD_PARTY_LINK)
        except NoSuchElementException:
            return None

    def find_remove_additional_document_link(self):
        try:
            return self.driver.find_element_by_id(self.REMOVE_ADDITIONAL_DOCUMENT_LINK)
        except NoSuchElementException:
            return None

    def does_remove_additional_document_exist(self, driver):
        return element_with_id_exists(driver, self.REMOVE_ADDITIONAL_DOCUMENT_LINK)

    def confirm_delete_additional_document(self):
        self.driver.find_element_by_id(self.DELETE_ADDITIONAL_DOC_CONFIRM_YES).click()
        functions.click_submit(self.driver)

    def click_application_locations_link(self):
        self.driver.execute_script("document.getElementById('" + self.LOCATION_LINK + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.LOCATION_LINK).click()

    def click_goods_type_link(self):
        self.driver.execute_script("document.getElementById('" + self.OPEN_GOODS_LINK + "').scrollIntoView(true);")
        element = self.driver.find_element_by_id(self.OPEN_GOODS_LINK)
        self.driver.execute_script("arguments[0].click();", element)

    def click_end_user_link(self):
        self.driver.find_element_by_id(self.LINK_END_USER_ID).click()

    def click_consignee_link(self):
        self.driver.find_element_by_id(self.LINK_CONSIGNEE_ID).click()

    def click_goods_countries_link(self):
        self.driver.execute_script(
            "document.getElementById('" + self.LINK_COUNTRIES_MATRIX_ID + "').scrollIntoView(true);"
        )
        self.driver.find_element_by_id(self.LINK_COUNTRIES_MATRIX_ID).click()

    def get_text_of_end_user_table(self):
        return self.driver.find_elements_by_css_selector(self.GOV_TABLES)[
            len(self.driver.find_elements_by_css_selector(self.GOV_TABLES)) - 1
        ].text

    def click_delete_end_user_document(self):
        self.driver.find_element_by_id(self.DELETE_END_USER_DOCUMENT).click()

    def attach_end_user_document_is_present(self):
        return self.driver.find_elements_by_id(self.ATTACH_END_USER_DOCUMENT)

    def get_text_of_lite_task_list_items(self):
        return self.driver.find_element_by_css_selector(self.LITE_TASK_LIST_ITEMS).text
