from pytest_bdd import when, then, parsers, scenarios

from pages.add_end_user_advisory_pages import AddEndUserAdvisoryPages
from pages.end_user_advisory_page import EndUserAdvisoryPage
from pages.shared import Shared

scenarios('../features/end_user_advisory_queries.feature', strict_gherkin=False)


@when('I select to create a new advisory')
def apply_for_end_user_advisory(driver):
    end_user_advisory_page = EndUserAdvisoryPage(driver)
    end_user_advisory_page.click_apply_for_advisories()
    Shared(driver).click_continue()


@when(parsers.parse('I select "{type}" user type and continue'))
def select_end_user_type(driver, type):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.select_type(type, prefix)
    Shared(driver).click_continue()


@when(parsers.parse('I enter "{name}" for the name'))
def add_user_details(driver, name):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.enter_name(name, prefix)
    Shared(driver).click_continue()


@when(parsers.parse('I enter "{nature}" for the nature of business'))
def add_user_details(driver, nature):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_nature(nature)
    Shared(driver).click_continue()


@when(parsers.parse('I enter "{name}" for the primary contact name, "{job}" for primary contact_job_title, "{email}" for the primary contact email, "{telephone}" for the primary contact telephone'))
def add_user_details(driver, name, email, telephone, job):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_primary_contact_email(email)
    end_user_page.enter_primary_contact_name(name)
    end_user_page.enter_primary_contact_job_title(job)
    end_user_page.enter_primary_contact_telephone(telephone)
    Shared(driver).click_continue()


@when(parsers.parse('I enter "{address}" for the address, "{country}" as the country and continue'))
def add_user_details(driver, address, country):
    end_user_page = AddEndUserAdvisoryPages(driver)
    prefix = "end_user."
    end_user_page.enter_address(address, prefix)
    end_user_page.enter_country(country, prefix)
    Shared(driver).click_continue()


@when(parsers.parse('I enter "{reasoning}" for my reason, and "{notes}" for notes and click submit'))
def enter_advisory_details(driver, reasoning, notes):
    end_user_page = AddEndUserAdvisoryPages(driver)
    end_user_page.enter_reasoning(reasoning)
    end_user_page.enter_notes(notes)
    Shared(driver).click_continue()


@then('I am given a confirmed submitted page, and am shown a 10 digit code')
def confirm_submitted_page_code(driver):
    end_user_page = AddEndUserAdvisoryPages(driver)
    assert len(end_user_page.confirmation_code()) == 10


@when("I click copy on an existing end user advisory")
def click_copy(driver):
    driver.find_elements_by_link_text('Copy')[0].click()


@when(parsers.parse('I enter "{name}" for the name and continue'))
def enter_name(driver, name):
    prefix = "end_user."
    AddEndUserAdvisoryPages(driver).enter_name(name, prefix)
    Shared(driver).click_continue()
