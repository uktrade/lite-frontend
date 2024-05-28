from selenium.webdriver.common.by import By

from ui_tests.caseworker.pages.BasePage import BasePage

from caseworker.search.forms import product_filters


class ProductSearchPage(BasePage):
    def enter_search_text(self, text):
        el = self.driver.find_element(by=By.XPATH, value="//input[@name='search_string']")
        el.clear()
        el.send_keys(text)

    def get_current_suggestions(self):
        suggestions = []
        reverse_product_filters = {v: k for k, v in product_filters.items()}
        table = self.driver.find_element(by=By.ID, value="autoComplete_list")
        for row in table.find_elements(by=By.CLASS_NAME, value="query-search__suggest-results-row"):
            key = row.find_element(by=By.CLASS_NAME, value="query-search__suggest-results-key").text
            value = row.find_element(by=By.CLASS_NAME, value="query-search__suggest-results-value").text
            suggestions.append({"key": reverse_product_filters[key], "value": value})

        return suggestions

    def select_suggestion(self, field, value):
        suggestions = self.get_current_suggestions()
        for index, s in enumerate(suggestions):
            if s["key"] == field and s["value"] == value:
                break

        table = self.driver.find_element(by=By.ID, value="autoComplete_list")
        suggestion_row = table.find_elements(by=By.CLASS_NAME, value="query-search__suggest-results-row")[index]
        suggestion_row.click()

    def get_result_row_data(self, result_row):
        data = {}

        data["name"] = result_row.find_element(by=By.CLASS_NAME, value="search-result__product-name").text
        data["applicant"] = result_row.find_element(by=By.CLASS_NAME, value="search-result__company-name").text
        data["part_number"] = result_row.find_element(by=By.CLASS_NAME, value="search-result__part-number").text

        details_table = result_row.find_element(by=By.CLASS_NAME, value="govuk-table")
        headings = details_table.find_elements(by=By.CLASS_NAME, value="govuk-table__header")
        values = details_table.find_elements(by=By.CLASS_NAME, value="govuk-table__cell")
        for head, cell in zip(headings, values):
            key = head.get_attribute("textContent").strip()
            value = cell.get_attribute("textContent").strip()

            if key in ["Destination", "Control list entry", "Regime"]:
                value = [item for item in cell.text.split("\n") if item != ""]

            data[key] = value

        return data
