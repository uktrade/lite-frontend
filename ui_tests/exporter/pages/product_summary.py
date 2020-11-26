from ui_tests.exporter.pages.BasePage import BasePage


class ProductSummary(BasePage):
    def get_page_heading(self):
        return self.driver.find_element_by_class_name("govuk-heading-l").text

    def get_summary_details(self):
        summary = {}
        for row in self.driver.find_elements_by_class_name("govuk-summary-list__row"):
            key = row.find_element_by_class_name("govuk-summary-list__key").text
            value = row.find_element_by_class_name("govuk-summary-list__value").text
            summary[key] = value

        return summary

    def get_field_details(self, field_name):
        for row in self.driver.find_elements_by_class_name("govuk-summary-list__row"):
            key = row.find_element_by_class_name("govuk-summary-list__key").text
            value = row.find_element_by_class_name("govuk-summary-list__value").text
            if key == field_name:
                link_element = row.find_element_by_xpath("dd[@class='govuk-summary-list__actions']/a")

                # in some cases we have additional details in the value, skip that
                return value.split("\n")[0], link_element

        return None, None
