from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.picklist_pages import PicklistPages
from pytest_bdd import scenarios, when, then, parsers
import shared.tools.helpers as utils

scenarios("../features/picklists.feature", strict_gherkin=False)


@when("I go to My Team")
def i_go_to_my_team(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_my_team()


@when("I go to picklists tab")
def i_go_to_picklists_tab(driver):
    PicklistPages(driver).click_on_picklist_tab()


@when("I deactivate my picklist")
def deactivate_picklist(driver):
    PicklistPages(driver).click_on_picklist_edit_button()
    PicklistPages(driver).click_on_picklist_deactivate_button()
    Shared(driver).click_submit()


@when("I reactivate my picklist")
def reactivate_picklist(driver):
    PicklistPages(driver).click_on_picklist_edit_button()
    PicklistPages(driver).click_on_picklist_reactivate_button()
    Shared(driver).click_submit()


@when(parsers.parse('I go to "{picklist_type}" picklist'))
def go_to_picklist_list(driver, picklist_type, context):
    context.picklist_type = picklist_type
    PicklistPages(driver).click_on_picklist_type_sub_nav(picklist_type)


@when(parsers.parse('I add a new picklist item with "{picklist_name}" and "{picklist_description}"'))
def add_to_picklist_item(driver, picklist_name, picklist_description, context):
    time = utils.get_formatted_date_time_m_d_h_s()
    context.picklist_name = picklist_name + time
    context.picklist_description = picklist_description + time
    PicklistPages(driver).type_into_picklist_name(context.picklist_name)
    PicklistPages(driver).type_into_picklist_description(context.picklist_description)


@then("I see my new picklist item in the list")
def see_new_picklist(driver, context):
    picklist_page = PicklistPages(driver)
    latest_picklist_name = picklist_page.get_latest_picklist_name()
    latest_picklist_description = picklist_page.get_latest_picklist_description()
    assert context.picklist_name in latest_picklist_name, "picklist name is not in column"
    assert context.picklist_description in latest_picklist_description, "picklist description is not in column"
    assert context.prompted_context_variable in latest_picklist_description, "picklist context variable not in column"


@then("I see picklist error messages")
def i_see_picklist_error_messages(driver, context):
    assert "Enter a name that best describes this template" in Shared(driver).get_text_of_error_message(
        0
    ), "picklist error message is not displayed"
    assert "Enter some text to use as a template" in Shared(driver).get_text_of_error_message(
        1
    ), "picklist error message is not displayed"


@when("I click on my picklist item")
def click_on_picklist_item(driver, context):
    elements = PicklistPages(driver).get_elements_of_picklist_names_in_list()
    no = utils.get_element_index_by_text(elements, context.picklist_name)
    elements[no].click()


@when(parsers.parse('I edit my picklist to "{picklist_name}" and "{picklist_description}"'))
def edit_picklist_item(driver, context, picklist_name, picklist_description):
    context.picklist_name = picklist_name
    context.picklist_description = picklist_description
    PicklistPages(driver).click_on_picklist_edit_button()
    PicklistPages(driver).type_into_picklist_name(context.picklist_name)
    PicklistPages(driver).type_into_picklist_description(context.picklist_description)
    Shared(driver).click_submit()


@then(parsers.parse('I see my picklist page with status as "{status}"'))
def i_see_my_picklist_page(driver, context, status):
    body = PicklistPages(driver).get_text_of_picklist_page_body()
    assert context.picklist_name in body, "picklist name is not displayed"
    assert context.picklist_description in body, "picklist description is not displayed"
    assert "Created by" in body, "created by is not displayed"
    if status == "Deactivated":
        assert driver.find_element_by_css_selector(".lite-tag").is_displayed()
    elif status == "Active":
        driver.set_timeout_to(0)
        assert len(driver.find_elements_by_css_selector(".lite-tag")) == 0
        driver.set_timeout_to_10_seconds()
    assert "Last updated" in body, "last updated is not displayed"
    assert context.picklist_type.lower().replace("_", " ") in body.lower().replace(
        "_", " "
    ), "picklist type is not displayed"


@when("I type {{ into the description")
def type_context_variable_start(driver, context):
    PicklistPages(driver).type_into_picklist_description(" {")


@then("I am given context variable suggestions")
def context_variable_overlay(driver):
    assert PicklistPages(driver).context_suggestions_are_displayed(), "Context variable suggestion list didn't appear"


@when("I click a suggested context variable")
def context_variable_option(driver, context):
    picklist_page = PicklistPages(driver)
    context.prompted_context_variable = picklist_page.get_context_suggestion_variable_name().split("\n")[0]
    picklist_page.click_context_suggestion()


@when("I click add a new picklist")
def click_add_picklist(driver):
    PicklistPages(driver).click_on_picklist_add_button()


@then(parsers.parse('An invalid variable error for "{variable_name}" is shown'))
def context_variable_error(driver, variable_name):
    assert variable_name in PicklistPages(driver).get_errors()


@when("I clear the picklist name and description")
def clear_picklist_name_and_description(driver):
    PicklistPages(driver).clear_picklist_name_and_description()
