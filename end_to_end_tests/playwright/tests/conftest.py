import os
import logging

import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict
from playwright.sync_api import Page, expect


logger = logging.getLogger(__name__)

DOTENV = os.path.join(os.path.dirname(__file__), "../.env")


class EnvironmentConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", validate_default=False, env_file=DOTENV)
    caseworker_url: str = "http://caseworker:8200/"
    exporter_url: str = "http://exporter:8300/"
    exporter_email: str = "foo@bar.com"  # /PS-IGNORE
    caseworker_email: str = "foo@bar.gov.uk"  # /PS-IGNORE


@pytest.fixture
def env_config():
    return EnvironmentConfig()


class PlaywrightTestCase:
    """
    A base test case for any generic helper functions for end to end tests.
    """

    @pytest.fixture(autouse=True)
    def setup(self, env_config: EnvironmentConfig, page: Page):
        self.env_config = env_config
        self.page = page

    def exporter_login(self):
        self.page.goto(self.env_config.exporter_url)
        self.page.get_by_role("button", name="Start now").click()
        self.page.get_by_label("Email").click()
        self.page.get_by_label("Email").fill(self.env_config.exporter_email)
        self.page.get_by_role("button", name="Continue").click()
        if self.page.url.endswith("/register-name/"):
            self.page.get_by_label("First name").fill("TEST")  # /PS-IGNORE
            self.page.get_by_label("Last name").fill("USER")  # /PS-IGNORE
            self.page.get_by_role("button", name="Continue").click()

        self.page.get_by_label("Archway Communications").check()
        self.page.get_by_role("button", name="Continue").click()

    def exporter_logout(self):
        self.page.get_by_role("link", name="Sign out").click()
        expect(self.page.get_by_text("Skip to main content GOV.UK")).to_be_visible()

    def caseworker_logout(self):
        self.page.get_by_role("link", name="Sign out").click()

    def caseworker_login(self):
        self.page.goto(self.env_config.caseworker_url)
        self.page.get_by_label("Email").fill(self.env_config.caseworker_email)
        self.page.get_by_role("button", name="Continue").click()

    def caseworker_super_user_change_teams(self, team_id, default_queue_id):
        self.page.locator("#link-profile").click()
        self.page.get_by_role("link", name="Change Team").click()
        self.page.get_by_label("Team").select_option(team_id)  # /PS-IGNORE
        self.page.get_by_label("Default Queue").select_option(default_queue_id)
        self.page.get_by_role("button", name="Save and return").click()
        self.page.get_by_role("link", name="Licensing for International").click()
