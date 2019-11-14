from selenium.common.exceptions import NoSuchElementException

from shared import functions


class ApplicationOverviewPage:

    def __init__(self, driver):
        self.driver = driver
        self.location_link = "location"
        self.hmrc_location_link = "goods_locations"
        self.hmrc_describe_your_goods = "describe_your_goods"
        self.hmrc_set_end_user = "set_end_user"
        self.hmrc_explain_your_reasoning = "explain_the_reason_behind_your_query"
        self.countries_link = "countries"
        self.standard_goods_link = "standard-goods"
        self.open_goods_link = "open-goods"
        self.end_user_link = "end_users"   # ID
        self.consignees_link = "consignees"
        self.ultimate_end_user_link = "ultimate_end_users"   # ID
        self.third_parties = "third_parties"  # ID
        self.sites_link = "a[href*='sites']"
        self.goods_on_application = "[id^=good-on-application-row]"  # CSS
        self.ultimate_end_users = "[id^=ultimate-end-user-row]" # CSS
        self.gov_tables = ".govuk-table__body"   # CSS
        self.attach_end_user_document_link = "attach_doc"  # ID
        self.download_end_user_document = "end_user_document_download"  # ID
        self.delete_end_user_document = "end_user_document_delete"  # ID
        self.end_user_document_state = "end_user_document_state"  # ID
        self.attach_end_user_document = "end_user_attach_doc"  # ID
        self.attach_consignee_document = "consignee_attach_doc"  # ID
        self.download_consignee_document = "consignee_document_download"  # ID
        self.delete_consignee_document = "consignee_document_delete"  # ID
        self.goods_countries_link = "goods_country_assignments"  # ID
        self.remove_good_link = "a[href*='good-on-application']"
        self.remove_goods_type_link = "a[href*='goods-types/remove']"
        self.remove_end_user_link = "a[href*='end-user/remove']"
        self.remove_consignee_link = "a[href*='consignee/remove']"
        self.remove_third_party_link = "a[href*='remove']"
        self.remove_additional_document_link = "document_delete"  # ID
        self.lite_task_list_items = ".lite-task-list__items"
        self.delete_additional_doc_confirm_yes = "delete_document_confirmation-yes"  # ID

    def find_remove_goods_type_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.remove_goods_type_link)
        except NoSuchElementException:
            return None

    def find_remove_good_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.remove_good_link)
        except NoSuchElementException:
            return None

    def find_remove_end_user_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.remove_end_user_link)
        except NoSuchElementException:
            return None

    def find_remove_consignee_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.remove_consignee_link)
        except NoSuchElementException:
            return None

    def find_remove_third_party_link(self):
        try:
            return self.driver.find_element_by_css_selector(self.remove_third_party_link)
        except NoSuchElementException:
            return None

    def find_remove_additional_document_link(self):
        try:
            return self.driver.find_element_by_id(self.remove_additional_document_link)
        except NoSuchElementException:
            return None

    def confirm_delete_additional_document(self):
        self.driver.find_element_by_id(self.delete_additional_doc_confirm_yes).click()
        functions.click_submit(self.driver)

    def click_third_parties(self):
        self.driver.find_element_by_id(self.third_parties).click()

    def click_application_locations_link(self):
        self.driver.execute_script("document.getElementById('" + self.location_link + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.location_link).click()

    def click_hmrc_application_locations_link(self):
        self.driver.find_element_by_id(self.hmrc_location_link).click()

    def click_hmrc_describe_your_goods(self):
        self.driver.find_element_by_id(self.hmrc_describe_your_goods).click()

    def click_hmrc_set_end_user(self):
        self.driver.find_element_by_id(self.hmrc_set_end_user).click()

    def click_hmrc_explain_your_reasoning(self):
        self.driver.find_element_by_id(self.hmrc_explain_your_reasoning).click()

    def click_standard_goods_link(self):
        self.driver.execute_script("document.getElementById('" + self.standard_goods_link + "').scrollIntoView(true);")
        element = self.driver.find_element_by_id(self.standard_goods_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_open_goods_link(self):
        self.driver.execute_script("document.getElementById('" + self.open_goods_link + "').scrollIntoView(true);")
        element = self.driver.find_element_by_id(self.open_goods_link)
        self.driver.execute_script("arguments[0].click();", element)

    def click_sites_link(self):
        self.driver.find_element_by_css_selector(self.sites_link).click()

    def click_end_user_link(self):
        self.driver.find_element_by_id(self.end_user_link).click()

    def click_ultimate_end_user_link(self):
        self.driver.find_element_by_id(self.ultimate_end_user_link).click()

    def click_consignee_link(self):
        self.driver.find_element_by_id(self.consignees_link).click()

    def click_countries_link(self):
        self.driver.execute_script("document.getElementById('" + self.countries_link + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.countries_link).click()

    def click_goods_countries_link(self):
        self.driver.execute_script("document.getElementById('" + self.goods_countries_link + "').scrollIntoView(true);")
        self.driver.find_element_by_id(self.goods_countries_link).click()

    def get_text_of_end_user_table(self):
        return self.driver.find_elements_by_css_selector(self.gov_tables)[len(self.driver.find_elements_by_css_selector(self.gov_tables))-1].text

    def get_text_of_good(self, index=0):
        return self.driver.find_elements_by_css_selector(self.goods_on_application)[index].text

    def get_ultimate_end_users(self):
        return self.driver.find_elements_by_css_selector(self.ultimate_end_users)

    def get_end_user_document_state_text(self):
        return self.driver.find_element_by_id(self.end_user_document_state).text

    def click_attach_end_user_document(self):
        self.driver.find_element_by_id(self.attach_end_user_document).click()

    def click_attach_consignee_document(self):
        self.driver.find_element_by_id(self.attach_consignee_document).click()

    def click_delete_end_user_document(self):
        self.driver.find_element_by_id(self.delete_end_user_document).click()

    def attach_end_user_document_is_present(self):
        return self.driver.find_elements_by_id(self.attach_end_user_document)

    def click_delete_consignee_document(self):
        self.driver.find_element_by_id(self.delete_consignee_document).click()

    def attach_consignee_document_is_present(self):
        return self.driver.find_elements_by_id(self.attach_consignee_document)

    def get_text_of_lite_task_list_items(self):
        return self.driver.find_element_by_css_selector(self.lite_task_list_items).text
