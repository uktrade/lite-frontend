from pytest_bdd import scenarios, when, then

from pages.additional_contacts import AdditionalContactsPage
from pages.application_page import ApplicationPage
from pages.shared import Shared
from faker import Faker

from shared import functions

fake = Faker()

scenarios("../features/additional_contacts.feature", strict_gherkin=False)


@when("I click on the additional contacts button")
def i_click_additional_contacts_button(driver, context):
    ApplicationPage(driver).click_additional_contacts_link()


@when("I click the add button")
def i_click_the_add_button(driver, context):
    AdditionalContactsPage(driver).click_add_button()


@when("I fill in the details and submit")
def i_fill_in_the_details_and_submit(driver, context):
    additional_contacts_page = AdditionalContactsPage(driver)
    context.additional_contact_email = fake.email()

    additional_contacts_page.enter_details(fake.prefix())
    additional_contacts_page.enter_name(fake.name())
    additional_contacts_page.enter_address(fake.address())
    additional_contacts_page.enter_country("United Kingdom")
    additional_contacts_page.enter_email(context.additional_contact_email)
    additional_contacts_page.enter_phone_number(fake.phone_number())

    functions.click_submit(driver)


@then("I can see the new contact in the list")
def i_can_see_the_new_contact_in_the_list(driver, context):
    assert context.additional_contact_email in Shared(driver).get_text_of_table()
