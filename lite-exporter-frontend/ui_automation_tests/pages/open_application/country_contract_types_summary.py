from faker import Faker

from ui_automation_tests.pages.BasePage import BasePage

fake = Faker()


class OpenApplicationCountryContractTypesSummaryPage(BasePage):
    RADIOBUTTON_ALL_COUNTRIES = "choice-all"

    OTHER_CONTRACT_TYPE_INPUT_ID = "other_contract_type_text"
    SUMMARY_LIST_COUNTRY_COLUMN_CLASS = ".govuk-summary-list__key"
    SUMMARY_LIST_CONTRACT_TYPES_COLUMN_CLASS = ".govuk-summary-list__value"

    def get_entries_from_summary_list_column(self, column_class):
        entries = []
        elements_in_column = self.driver.find_elements_by_css_selector(column_class)
        for entry in elements_in_column:
            entries.append(entry.text)
        return entries

    def get_countries_with_respective_contract_types(self):
        countries_on_summary = self.get_entries_from_summary_list_column(self.SUMMARY_LIST_COUNTRY_COLUMN_CLASS)
        contract_types_per_country_on_summary = self.get_entries_from_summary_list_column(
            self.SUMMARY_LIST_CONTRACT_TYPES_COLUMN_CLASS
        )
        countries_with_respective_contract_types = list(
            zip(countries_on_summary, contract_types_per_country_on_summary)
        )
        return countries_with_respective_contract_types
