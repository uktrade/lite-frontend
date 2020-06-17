from pytest_bdd import scenarios, then

from pages.application_page import ApplicationPage
from pages.shared import Shared

scenarios("../features/manage_cases.feature", strict_gherkin=False)
