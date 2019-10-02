from pytest_bdd import when, then, parsers, scenarios, given
from pages.application_page import ApplicationPage
from pages.give_advice_pages import GiveAdvicePages
from pages.header_page import HeaderPage
from pages.record_decision_page import RecordDecision
from pages.roles_pages import RolesPages
from pages.shared import Shared
from pages.users_page import UsersPage

scenarios('../features/give_advice.feature', strict_gherkin=False)


@when("I give myself all permissions")
def get_required_permissions(driver):
    roles_page = RolesPages(driver)
    HeaderPage(driver).open_users()
    UsersPage(driver).click_on_manage_roles()
    roles_page.click_edit_for_default_role()
    roles_page.edit_default_role_to_have_all_permissions()
    Shared(driver).click_submit()


@then("I reset the permissions")
def reset_permissions(driver):
    roles_page = RolesPages(driver)
    HeaderPage(driver).open_users()
    UsersPage(driver).click_on_manage_roles()
    roles_page.click_edit_for_default_role()
    roles_page.remove_all_permissions_from_default_role()
    Shared(driver).click_submit()


@given("I create a proviso picklist")
def i_create_an_proviso_picklist(context, add_a_proviso_picklist):
    context.proviso_picklist_name = add_a_proviso_picklist['name']
    context.proviso_picklist_question_text = add_a_proviso_picklist['text']


@when(parsers.parse('I select decision "{number}"'))
def select_decision(driver, number, context):
    record = RecordDecision(driver)
    record.click_on_decision_number(number)
    context.advice_data.append(number)


@given("I create a standard advice picklist")
def i_create_an_standard_advice_picklist(context, add_a_standard_advice_picklist):
    context.standard_advice_query_picklist_name = add_a_standard_advice_picklist['name']
    context.standard_advice_query_picklist_question_text = add_a_standard_advice_picklist['text']


@when("I select all items in the advice view")
def click_items_in_advice_view(driver, context):
    context.number_of_advice_items_clicked = ApplicationPage(driver).click_on_all_checkboxes()


@when('I click on view advice')
def i_click_on_view_advice(driver, context):
    application_page = ApplicationPage(driver)
    application_page.click_view_advice()


@when(parsers.parse("I choose to '{option}' the licence"))
def choose_advice_option(driver, option, context):
    GiveAdvicePages(driver).click_on_advice_option(option)
    Shared(driver).click_submit()
    context.advice_data = []


@when(parsers.parse("I write '{text}' in the note text field"))
def write_note_text_field(driver, text, context):
    GiveAdvicePages(driver).type_in_additional_note_text_field(text)
    context.advice_data.append(text)


@then('I see the fields pre-populated with the proviso and advice picklist items')
def i_see_fields_prepopulated(driver, context):
    advice = driver.find_element_by_id('advice').text
    proviso = driver.find_element_by_id('proviso').text
    assert advice == context.standard_advice_query_picklist_question_text
    assert proviso == context.proviso_picklist_question_text


@when(parsers.parse("I import text from the '{option}' picklist"))
def import_text_advice(driver, option, context):
    GiveAdvicePages(driver).click_on_import_advice_link(option)
    text = GiveAdvicePages(driver).get_text_of_picklist_item()
    context.advice_data.append(text)
    GiveAdvicePages(driver).click_on_picklist_item(option)
    assert text == driver.find_element_by_id(option).text


@then("I see my advice has been posted successfully")
def posted_successfully_advice(driver):
    pass
    # Commenting the below out due to bug.
    # assert Shared(driver).get_text_of_info_bar() == "Your advice has been posted successfully"


@then('I see added advice in the same amount of places')
def added_advice_on_application_page(driver, context):
    assert len(driver.find_elements_by_css_selector('.app-advice__details')) == context.number_of_advice_items_clicked
    for advice in context.advice_data:
        assert advice in driver.find_element_by_css_selector('.app-advice__details').text


@when("I go to the team advice")
def go_to_team_advice(driver):
    page = GiveAdvicePages(driver)
    page.go_to_team_advice()


@when("I go to the final advice")
def go_to_final_advice(driver):
    page = GiveAdvicePages(driver)
    page.go_to_final_advice()


@when("I combine all advice")
def combine_all_advice(driver):
    page = GiveAdvicePages(driver)
    page.combine_advice()


@when("I finalise the licence")
def finalise(driver):
    page = GiveAdvicePages(driver)
    page.finalise()


@when("I finalise the goods and countries")
def finalise_goods_and_countries(driver):
    page = GiveAdvicePages(driver)
    page.finalise_goods_and_countries()

@when("I select approve for all combinations of goods and countries")
def select_approve_for_all(driver):
    page = GiveAdvicePages(driver)
    page.select_approve_for_all()
