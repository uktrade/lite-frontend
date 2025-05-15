import os
import logging
from typing import Any, Dict

import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict
from playwright.sync_api import Page, expect


logger = logging.getLogger(__name__)

DOTENV = os.path.join(os.path.dirname(__file__), "../.env")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: Dict[str, Any]) -> Dict[str, Any]:
    return {**browser_context_args, "viewport": {"width": 1920, "height": 1080}}


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
        self.page.get_by_role("button", name="Continue").click()
        self.page.get_by_label("Archway Communications").check()
        self.page.get_by_role("button", name="Continue").click()

    def exporter_logout(self):
        self.page.get_by_role("link", name="Sign out").click()
        expect(self.page.get_by_text("Skip to main content GOV.UK")).to_be_visible()
