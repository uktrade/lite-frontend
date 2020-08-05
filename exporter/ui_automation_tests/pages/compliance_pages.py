from ui_automation_tests.pages.BasePage import BasePage
from ui_automation_tests.shared.tools.helpers import find_paginated_item_by_id


class CompliancePages(BasePage):
    PARTIAL_SITE_CASE_LIST_LINK_ID = "case-"
    PARTIAL_VISIT_CASE_LIST_LINK_ID = "visit-"
    TAB_DETAILS_ID = "link-details"
    TAB_ECJU_QUERIES_ID = "link-ecju-queries"
    TAB_NOTES_ID = "link-case-notes"
    TAB_GENERATED_DOCUMENTS_ID = "link-generated-documents"
    TAB_VISITS_ID = "link-visits"

    def find_paginated_compliance_site_case_row(self, case_id):
        return find_paginated_item_by_id(case_id, self.driver)

    def find_paginated_compliance_visit_case(self, case_id):
        return find_paginated_item_by_id(case_id, self.driver)

    def view_compliance_case(self, case_id):
        self.driver.find_element_by_id(f"{self.PARTIAL_SITE_CASE_LIST_LINK_ID}{case_id}").click()

    def view_visit_case(self, case_id):
        self.driver.find_element_by_id(f"{self.PARTIAL_VISIT_CASE_LIST_LINK_ID}{case_id}").click()

    def details_tab(self):
        return self.driver.find_element_by_id(self.TAB_DETAILS_ID)

    def ecju_queries_tab(self):
        return self.driver.find_element_by_id(self.TAB_ECJU_QUERIES_ID)

    def notes_tab(self):
        return self.driver.find_element_by_id(self.TAB_NOTES_ID)

    def generated_documents_tab(self):
        return self.driver.find_element_by_id(self.TAB_GENERATED_DOCUMENTS_ID)

    def visits_tab(self):
        return self.driver.find_element_by_id(self.TAB_VISITS_ID)
