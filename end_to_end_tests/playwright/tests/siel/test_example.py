from end_to_end_tests.playwright.tests.siel.base import SIELTestCase


class TestExample(SIELTestCase):

    def test_example(self):
        self.exporter_login()
        self.create_application()
        self.exporter_logout()

        self.caseworker_login()
        self.manage_application()
        self.caseworker_logout()

    def create_application(self):
        self.page.goto(self.env_config.exporter_url)

    def manage_application(self):
        self.page.goto(self.env_config.caseworker_url)
