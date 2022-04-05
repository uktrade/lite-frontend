from selenium.webdriver.common.by import By

from ui_tests.exporter.pages.BasePage import BasePage


class CheckYourAnswers(BasePage):
    APPLICATION_SUMMARY_ID = "application-summary-grid"

    def get_summary_row_value(self, label):
        return self.driver.find_element(
            by=By.XPATH, value=f"//div[@id='{self.APPLICATION_SUMMARY_ID}']//div[contains(., '{label}')]//dd"
        ).text

    def get_row_value(self, label):
        return self.driver.find_element(
            by=By.XPATH, value=f"//div//dt[contains(text(), '{label}')]//following-sibling::dd"
        ).text

    def get_product_field_value(self, column_name):
        product_table = self.driver.find_elements(By.XPATH, "//table[@class='govuk-table']")[0]
        columns = [element.text for element in product_table.find_elements(By.XPATH, ".//thead/tr/th")]
        rows = [element.text for element in product_table.find_elements(By.XPATH, ".//tbody/tr/td")]
        product_data = dict(zip(columns, rows))
        return product_data.get(column_name)

    def get_end_use_field_value(self, key):
        end_use_table = self.driver.find_elements(By.XPATH, "//table[@class='govuk-table']")[1]
        rows = [element.text for element in end_use_table.find_elements(By.XPATH, ".//tbody/tr/td")]
        end_use_data = {rows[i]: rows[i + 1] for i in range(1, len(rows), 3)}
        return end_use_data.get(key)

    def get_end_user_row_value(self, label):
        end_user_summary = self.driver.find_element(
            by=By.XPATH, value=f"//h2[contains(text(), 'End user')]//following-sibling::div"
        )
        return end_user_summary.find_element(
            by=By.XPATH, value=f".//div//dt[contains(text(), '{label}')]//following-sibling::dd"
        ).text

    def get_party_section_text(self, party_type):
        party_summary = self.driver.find_element(
            by=By.XPATH, value=f"//h2[contains(text(), '{party_type}')]//following-sibling::div"
        )
        return party_summary.text

    def get_notes_text(self):
        return self.driver.find_element(
            by=By.XPATH, value=f"//h2[contains(text(), 'Notes')]//following-sibling::p"
        ).text
