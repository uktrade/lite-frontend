from selenium.common.exceptions import NoSuchElementException

from shared import functions
from shared.BasePage import BasePage


class ApplicationOverviewPage(BasePage):

    LOCATION_LINK = "location"
    HMRC_LOCATION_LINK = "goods_locations"
    HMRC_DESCRIBE_YOUR_GOODS = "describe_your_goods"
    HMRC_SET_END_USER = "set_end_user"
    HMRC_EXPLAIN_YOUR_REASONING = "explain_the_reason_behind_your_query"
    LINK_COUNTRIES_ID = "set_countries"
    STANDARD_GOODS_LINK = "standard-goods"
    OPEN_GOODS_LINK = "open-goods"
    END_USER_LINK = "end_users"  # ID
    CONSIGNEES_LINK = "consignees"
    ULTIMATE_END_USER_LINK = "ultimate_end_users"  # ID
    THIRD_PARTIES = "third_parties"  # ID
    SITES_LINK = "a[href*='sites']"
    GOODS_ON_APPLICATION = "[id^=good-on-application-row]"  # CSS
    ULTIMATE_END_USERS = "[id^=ultimate-end-user-row]"  # CSS
    GOV_TABLES = ".govuk-table__body"  # CSS
    ATTACH_END_USER_DOCUMENT_LINK = "attach_doc"  # ID
    DOWNLOAD_END_USER_DOCUMENT = "end_user_document_download"  # ID
    DELETE_END_USER_DOCUMENT = "end_user_document_delete"  # ID
    END_USER_DOCUMENT_STATE = "end_user_document_state"  # ID
    ATTACH_END_USER_DOCUMENT = "end_user_attach_doc"  # ID
    ATTACH_CONSIGNEE_DOCUMENT = "consignee_attach_doc"  # ID
    DOWNLOAD_CONSIGNEE_DOCUMENT = "consignee_document_download"  # ID
    DELETE_CONSIGNEE_DOCUMENT = "consignee_document_delete"  # ID
    GOODS_COUNTRIES_LINK = "goods_country_assignments"  # ID
    REMOVE_GOOD_LINK = "a[href*='good-on-application']"
    REMOVE_GOODS_TYPE_LINK = "a[href*='goods-types/remove']"
    REMOVE_END_USER_LINK = "a[href*='end-user/remove']"
    REMOVE_CONSIGNEE_LINK = "a[href*='consignee/remove']"
    REMOVE_THIRD_PARTY_LINK = "a[href*='remove']"
    REMOVE_ADDITIONAL_DOCUMENT_LINK = "document_delete"  # ID
    LITE_TASK_LIST_ITEMS = ".lite-task-list__items"
    DELETE_ADDITIONAL_DOC_CONFIRM_YES = "delete_document_confirmation-yes"  # ID

    def find_remove_goods_type_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_GOODS_TYPE_LINK)
        except NoSuchElementException:
            return None

    def find_remove_good_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_GOOD_LINK)
        except NoSuchElementException:
            return None

    def find_remove_end_user_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_END_USER_LINK)
        except NoSuchElementException:
            return None

    def find_remove_consignee_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.REMOVE_CONSIGNEE_LINK)
        except NoSuchElementException:
            return None

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

    def confirm_delete_additional_document(self):
        self.driver.find_element_by_id(self.DELETE_ADDITIONAL_DOC_CONFIRM_YES).click()
        functions.click_submit(self.driver)

    def click_third_parties(self):
        self.driver.find_element_by_id(self.THIRD_PARTIES).click()

    def click_application_locations_link(self):
        self.driver.execute_script("document.getElementById('" + self.LOCATION_LINK + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.LOCATION_LINK).click()

    def click_hmrc_application_locations_link(self):
        self.driver.find_element_by_id(self.HMRC_LOCATION_LINK).click()

    def click_hmrc_describe_your_goods(self):
        self.driver.find_element_by_id(self.HMRC_DESCRIBE_YOUR_GOODS).click()

    def click_hmrc_set_end_user(self):
        self.driver.find_element_by_id(self.HMRC_SET_END_USER).click()

    def click_hmrc_explain_your_reasoning(self):
        self.driver.find_element_by_id(self.HMRC_EXPLAIN_YOUR_REASONING).click()

    def click_standard_goods_link(self):
        self.driver.execute_script("document.getElementById('" + self.STANDARD_GOODS_LINK + "').scrollIntoView(true);")
        element = self.driver.find_element_by_id(self.STANDARD_GOODS_LINK)
        self.driver.execute_script("arguments[0].click();", element)

    def click_open_goods_link(self):
        self.driver.execute_script("document.getElementById('" + self.OPEN_GOODS_LINK + "').scrollIntoView(true);")
        element = self.driver.find_element_by_id(self.OPEN_GOODS_LINK)
        self.driver.execute_script("arguments[0].click();", element)

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.SITES_LINK).click()

    def click_end_user_link(self):
        self.driver.find_element_by_id(self.END_USER_LINK).click()

    def click_ultimate_end_user_link(self):
        self.driver.find_element_by_id(self.ULTIMATE_END_USER_LINK).click()

    def click_consignee_link(self):
        self.driver.find_element_by_id(self.CONSIGNEES_LINK).click()

    def click_countries_link(self):
        self.driver.execute_script("document.getElementById('" + self.LINK_COUNTRIES_ID + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.LINK_COUNTRIES_ID).click()

    def click_goods_countries_link(self):
        self.driver.execute_script("document.getElementById('" + self.GOODS_COUNTRIES_LINK + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.GOODS_COUNTRIES_LINK).click()

    def get_text_of_end_user_table(self):
        return self.driver.find_elements_by_css_selector(self.GOV_TABLES)[
            len(self.driver.find_elements_by_css_selector(self.GOV_TABLES)) - 1
        ].text

    def get_text_of_good(self, index=0):
        return self.driver.find_elements_by_css_selector(self.GOODS_ON_APPLICATION)[index].text

    def get_ultimate_end_users(self):
        return self.driver.find_elements_by_css_selector(self.ULTIMATE_END_USERS)

    def get_end_user_document_state_text(self):
        return self.driver.find_element_by_id(self.END_USER_DOCUMENT_STATE).text

    def click_attach_end_user_document(self):
        self.driver.find_element_by_id(self.ATTACH_END_USER_DOCUMENT).click()

    def click_attach_consignee_document(self):
        self.driver.find_element_by_id(self.ATTACH_CONSIGNEE_DOCUMENT).click()

    def click_delete_end_user_document(self):
        self.driver.find_element_by_id(self.DELETE_END_USER_DOCUMENT).click()

    def attach_end_user_document_is_present(self):
        return self.driver.find_elements_by_id(self.ATTACH_END_USER_DOCUMENT)

    def click_delete_consignee_document(self):
        self.driver.find_element_by_id(self.DELETE_CONSIGNEE_DOCUMENT).click()

    def attach_consignee_document_is_present(self):
        return self.driver.find_elements_by_id(self.ATTACH_CONSIGNEE_DOCUMENT)

    def get_text_of_lite_task_list_items(self):
        return self.driver.find_element_by_css_selector(self.LITE_TASK_LIST_ITEMS).text
