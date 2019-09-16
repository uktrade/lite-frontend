from pytest_bdd import when, then, parsers, scenarios

from pages.add_end_user_advisory_pages import AddEndUserAdvisoryPages
from pages.end_user_advisory_page import EndUserAdvisoryPage

scenarios('../features/end_user_advisory_queries.feature', strict_gherkin=False)


@when('I select to create a new advisory')
def apply_for_end_user_advisory(driver):
    end_user_advisory_page = EndUserAdvisoryPage(driver)
    end_user_advisory_page.click_apply_for_advisories()


@when(parsers.parse('I select "{type}" user type and continue'))
def select_end_user_type(driver, type):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.select_type(type, prefix)
    end_user_page.click_continue()


@when(parsers.parse('I select "{name}" for the name, "{address}" for the address, "{country}" as the country, and continue'))
def add_user_details(driver, name, address, country):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.enter_name(name, prefix)
    end_user_page.enter_address(address, prefix)
    end_user_page.enter_country(country, prefix)
    end_user_page.click_continue()


@when(parsers.parse('I enter "{reasoning}" for my reason, and "{notes}" for notes and click submit'))
def enter_advisory_details(driver, reasoning, notes):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_reasoning(reasoning)
    end_user_page.enter_notes(notes)
    end_user_page.click_continue()


@then('I am given a confirmed submitted page, and am shown a 10 digit code')
def confirm_submitted_page_code(driver):
    end_user_page = AddEndUserAdvisoryPages(driver)
    assert len(end_user_page.confirmation_code()) == 10
