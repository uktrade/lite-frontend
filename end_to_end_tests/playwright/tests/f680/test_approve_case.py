from playwright.sync_api import expect

from end_to_end_tests.playwright.tests.utils import get_application_id, assert_page_url
from end_to_end_tests.playwright.tests.f680.base import F680TestCase


class TestApproveF680Case(F680TestCase):

    def test_approve_case(self):
        self.exporter_login()
        self.create_application()
        self.exporter_logout()

        self.caseworker_login()
        self.manage_application()
        self.caseworker_logout()

    def create_application(self):
        self.page.goto(self.env_config.exporter_url)

        self.page.get_by_role("link", name="Apply for a licence or").click()
        self.page.get_by_label("Form 680 (F680) security").check()
        self.page.get_by_role("button", name="Continue").click()

        self.app_pk = get_application_id(
            self.page.url,
            r"/f680/(?P<app_pk>([a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}))/apply/",
        )

        self.page.get_by_role("link", name="General application details").click()
        self.page.get_by_label("Name the application").click()
        self.page.get_by_label("Name the application").fill("TEST APPLICATION")
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_label("No").check()
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_label("No").check()
        self.page.get_by_role("button", name="Continue").click()

        self.page.get_by_role("link", name="Approval type").click()
        self.page.get_by_label("Initial discussions or").check()
        self.page.get_by_label("Demonstration in the United").check()
        self.page.get_by_label("Explain what you're demonstrating in the UK and why").click()
        self.page.get_by_label("Explain what you're demonstrating in the UK and why").fill("DEMO details in the UK")
        self.page.get_by_label("Demonstration overseas").check()

        self.page.get_by_label("Explain what you're demonstrating overseas and why").click()
        self.page.get_by_label("Explain what you're demonstrating overseas and why").fill("Demo overseas ")
        self.page.get_by_label("Training").check()
        self.page.get_by_label("Through life support").check()
        self.page.get_by_label("Supply").check()
        self.page.get_by_label("Provide details about what").click()
        self.page.get_by_label("Provide details about what").fill("Approval please")
        self.page.get_by_role("button", name="Save and continue").click()

        self.page.get_by_role("link", name="Product information").click()
        self.page.get_by_label("Give the item a descriptive").click()
        self.page.get_by_label("Give the item a descriptive").fill("PRODUCT 1")
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("Describe the item").click()
        self.page.get_by_label("Describe the item").fill("My product")
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("Yes").check()
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_label("NATO", exact=True).check()
        self.page.get_by_label("Confidential").check()
        self.page.get_by_label("Day").click()
        self.page.get_by_label("Day").fill("10")
        self.page.get_by_label("Day").press("Tab")
        self.page.get_by_label("Month").fill("10")
        self.page.get_by_label("Month").press("Tab")
        self.page.get_by_label("Year").fill("2022")
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("Name and address of the").click()
        self.page.get_by_label("Name and address of the").fill("MOD")
        self.page.get_by_label("Reference").click()
        self.page.get_by_label("Reference").fill("APPROVAL-1")
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("No").check()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("No").check()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("Don't know").check()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("Don't know").check()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("No").check()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("MOD", exact=True).check()
        self.page.get_by_text("Who is funding the item? MOD").click()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("Full name").click()
        self.page.get_by_label("Full name").fill("MOD")
        self.page.get_by_label("Address", exact=True).click()
        self.page.get_by_label("Address", exact=True).fill("MOD")
        self.page.get_by_label("Address", exact=True).click()
        self.page.get_by_label("Phone number").click()
        self.page.get_by_label("Phone number").fill("01234567890")
        self.page.get_by_label("Email address").click()
        self.page.get_by_label("Email address").fill("a@a.com")  # /PS-IGNORE
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("No").check()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_role("link", name="User information").click()
        self.page.get_by_label("End-user", exact=True).check()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("Name").click()
        self.page.get_by_label("Name").fill("TEST-USER1")
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("Address").click()
        self.page.get_by_label("Address").fill("Test user 1\nstreet")
        self.page.get_by_label("Country").click()
        self.page.get_by_role("option", name="Abu Dhabi").click()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("NATO", exact=True).check()
        self.page.get_by_label("SECRET", exact=True).check()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("How does the entity intend to").click()
        self.page.get_by_label("How does the entity intend to").fill("Integrate with something else")
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_role("button", name="Save and continue").click()
        self.page.get_by_label("Yes").check()
        self.page.get_by_role("button", name="Accept and submit").click()
        self.page.get_by_text("ECJU reference: F680/2025/").click()
        assert_page_url(self.page, f"/applications/{self.app_pk}/submit-success/")
        self.page.get_by_role("link", name="Back", exact=True).click()
        assert_page_url(self.page, f"/f680/{self.app_pk}/summary/")
        self.app_reference_code = self.page.locator("#summary-list-reference-code").text_content().strip()

    def manage_application(self):
        self.page.goto(self.env_config.caseworker_url)

        # MOD- ECJU / Default Queue
        self.caseworker_super_user_change_teams(
            "b7640925-2577-4c24-8081-b85bd635b62a", "00000000-0000-0000-0000-000000000001"  # /PS-IGNORE
        )

        self.page.get_by_role("link", name="All cases (Click to change").click()
        self.page.get_by_role("link", name="F680 Cases to review").click()
        self.page.locator(f"#case-{self.app_pk}").click()

        assert_page_url(self.page, f"/cases/{self.app_pk}/f680/details/")
        self.page.get_by_role("button", name="Allocate to me").click()
        self.page.get_by_role("button", name="Move case forward").click()

        # MOD- Caprot / Default Queue
        self.caseworker_super_user_change_teams(
            "a06aec31-47d7-443b-860d-66ab0c6d7cfd", "00000000-0000-0000-0000-000000000001"  # /PS-IGNORE
        )

        self.page.get_by_role("link", name="All cases (Click to change").click()
        self.page.get_by_role("link", name="MOD-CapProt cases to review").click()
        self.page.locator(f"#case-{self.app_pk}").click()
        assert_page_url(self.page, f"/cases/{self.app_pk}/f680/details/")
        self.page.get_by_role("button", name="Allocate to me").click()

        self.page.get_by_role("link", name="Recommendations").click()
        self.page.get_by_role("link", name="Make recommendation").click()
        self.page.get_by_label("TEST-USER1, Abu Dhabi").check()
        self.page.get_by_label("Approve").check()
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_label("Secret", exact=True).check()
        self.page.get_by_label("Provisos").click()
        self.page.get_by_label("Provisos").fill("SECRET PROVISOS")
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_role("button", name="Move case forward").click()

        # MOD - DI / Default Queue
        self.caseworker_super_user_change_teams(
            "2e5fab3c-4599-432e-9540-74ccfafb18ee", "00000000-0000-0000-0000-000000000001"  # /PS-IGNORE
        )

        self.page.get_by_role("link", name="All cases (Click to change").click()
        self.page.get_by_role("link", name="MOD-DI Indirect cases to review").click()
        self.page.locator(f"#case-{self.app_pk}").click()
        assert_page_url(self.page, f"/cases/{self.app_pk}/f680/details/")
        self.page.get_by_role("button", name="Allocate to me").click()

        self.page.get_by_role("link", name="Recommendations").click()
        self.page.get_by_role("link", name="Make recommendation").click()
        self.page.get_by_label("TEST-USER1, Abu Dhabi").check()
        self.page.get_by_label("Approve").check()
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_label("Secret", exact=True).check()
        self.page.get_by_label("Provisos").click()
        self.page.get_by_label("Provisos").fill("SECRET PROVISOS")
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_role("button", name="Move case forward").click()

        # MOD- DSR / Default Queue
        self.caseworker_super_user_change_teams(
            "4c62ce4a-18f8-4ada-8d18-4b53a565250f", "00000000-0000-0000-0000-000000000001"  # /PS-IGNORE
        )

        self.page.get_by_role("link", name="All cases (Click to change").click()
        self.page.get_by_role("link", name="MOD-DSR cases to review").click()
        self.page.locator(f"#case-{self.app_pk}").click()

        assert_page_url(self.page, f"/cases/{self.app_pk}/f680/details/")
        self.page.get_by_role("button", name="Allocate to me").click()

        self.page.get_by_role("link", name="Recommendations").click()
        self.page.get_by_role("link", name="Make recommendation").click()
        self.page.get_by_label("TEST-USER1, Abu Dhabi").check()
        self.page.get_by_label("Approve").check()
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_label("Secret", exact=True).check()
        self.page.get_by_label("Provisos").click()
        self.page.get_by_label("Provisos").fill("SECRET PROVISOS")
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_role("button", name="Move case forward").click()

        # MOD- ECJU / Default Queue
        self.caseworker_super_user_change_teams(
            "b7640925-2577-4c24-8081-b85bd635b62a", "00000000-0000-0000-0000-000000000001"  # /PS-IGNORE
        )

        self.page.get_by_role("link", name="All cases (Click to change").click()
        self.page.get_by_role("link", name="F680 Cases under final review").click()
        self.page.locator(f"#case-{self.app_pk}").click()
        assert_page_url(self.page, f"/cases/{self.app_pk}/f680/details/")
        self.page.get_by_role("button", name="Allocate to me").click()
        self.page.get_by_role("link", name="Recommendation").click()
        self.page.get_by_role("link", name="Decide outcome").click()

        self.page.get_by_label("TEST-USER1 - Abu Dhabi -").check()
        self.page.get_by_label("Approve").check()
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_label("Secret", exact=True).check()
        self.page.get_by_label("Initial discussions or").check()
        self.page.get_by_label("Demonstration in the United").check()
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_role("link", name="Generate letters").click()
        self.page.get_by_role("link", name="Generate").click()

        self.page.get_by_role("button", name="Generate").click()
        self.page.get_by_role("button", name="Finalise and publish to").click()
        expect(self.page.locator("dl")).to_contain_text("Finalised")
        expect(self.page.locator("#case-sub-status")).to_contain_text("Approved")
