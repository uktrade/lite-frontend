from pytest_bdd import scenarios, given, when, then, parsers
from selenium.webdriver.common.by import By
import helpers.helpers as utils
from pages.internal_hub_page.py import InternalHubPage

scenarios('../features/case_note.feature')