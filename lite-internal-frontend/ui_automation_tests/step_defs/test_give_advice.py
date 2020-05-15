from datetime import date

from pytest_bdd import when, then, parsers, scenarios, given

from pages.advice import UserAdvicePage, FinalAdvicePage, TeamAdvicePage, BaseAdvicePage
from pages.case_page import CasePage, CaseTabs
from pages.give_advice_pages import GiveAdvicePages
from pages.record_decision_page import RecordDecision
from pages.shared import Shared
from ui_automation_tests.pages.grant_licence_page import GrantLicencePage

scenarios("../features/give_advice.feature", strict_gherkin=False)


@given("I create a proviso picklist")
def i_create_an_proviso_picklist(context, add_a_proviso_picklist):
    context.proviso_picklist_name = add_a_proviso_picklist["name"]
    context.proviso_picklist_question_text = add_a_proviso_picklist["text"]


@when(parsers.parse('I select decision "{number}"'))
def select_decision(driver, number, context):
    record = RecordDecision(driver)
    record.click_on_decision_number(number)
    context.advice_data.append(number)


@given("I create a standard advice picklist")
def i_create_an_standard_advice_picklist(context, add_a_standard_advice_picklist):
    context.standard_advice_query_picklist_name = add_a_standard_advice_picklist["name"]
    context.standard_advice_query_picklist_question_text = add_a_standard_advice_picklist["text"]


@when("I select all items in the user advice view")
def click_items_in_advice_view(driver, context):
    context.number_of_advice_items_clicked = UserAdvicePage(driver).click_on_all_checkboxes()


@when("I select all items in the team advice view")
def click_items_in_advice_view(driver, context):
    context.number_of_advice_items_clicked = TeamAdvicePage(driver).click_on_all_checkboxes()


@when("I click on the user advice tab")
def i_click_on_view_advice(driver, context):
    CasePage(driver).change_tab(CaseTabs.USER_ADVICE)


@when(parsers.parse("I choose to '{option}' the licence"))
def choose_advice_option(driver, option, context):
    GiveAdvicePages(driver).click_on_advice_option(option)
    context.advice_data = []


@when(parsers.parse("I write '{text}' in the note text field"))
def write_note_text_field(driver, text, context):
    GiveAdvicePages(driver).type_in_additional_note_text_field(text)
    context.advice_data.append(text)


@then("I see the fields pre-populated with the proviso and advice picklist items")
def i_see_fields_prepopulated(driver, context):
    text = driver.find_element_by_id("text").text
    proviso = driver.find_element_by_id("proviso").text
    assert text == context.standard_advice_query_picklist_question_text
    assert proviso == context.proviso_picklist_question_text


@when(parsers.parse("I import text from the '{option}' picklist"))
def import_text_advice(driver, option, context):
    GiveAdvicePages(driver).click_on_import_link(option)
    text = GiveAdvicePages(driver).get_text_of_picklist_item()
    context.advice_data.append(text)
    GiveAdvicePages(driver).click_on_picklist_item(option)


@then("I see my advice has been posted successfully")
def posted_successfully_advice(driver):
    assert "Advice posted successfully" in Shared(driver).get_text_of_info_bar()


@then("I see added advice in the same amount of places")
def added_advice_on_application_page(driver, context):
    assert len(driver.find_elements_by_css_selector(".app-advice__item")) == context.number_of_advice_items_clicked
    for advice in context.advice_data:
        assert advice in driver.find_element_by_css_selector(".app-advice__item").text


@when("I go to the team advice")
def go_to_team_advice(driver):
    CasePage(driver).change_tab(CaseTabs.TEAM_ADVICE)


@when("I go to the final advice")
def go_to_final_advice(driver):
    CasePage(driver).change_tab(CaseTabs.FINAL_ADVICE)


@when("I finalise the goods and countries")
def finalise_goods_and_countries(driver):
    FinalAdvicePage(driver).click_finalise()


@when("I select approve for all combinations of goods and countries")
def select_approve_for_all(driver):
    page = GiveAdvicePages(driver)
    page.select_approve_for_all()


@then("today's date and duration is filled in")
def todays_date_is_filled_in(driver):
    date_in_form = GrantLicencePage(driver).get_date_in_date_entry()
    today = date.today()
    assert today.day == int(date_in_form["day"])
    assert today.month == int(date_in_form["month"])
    assert today.year == int(date_in_form["year"])

    duration_in_form = GrantLicencePage(driver).get_duration_in_finalise_view()

    assert int(duration_in_form) > 0


@then("I see refusal flag is attached")
def refusal_flag_displayed(driver):
    assert Shared(driver).is_flag_applied("Refusal Advice")


@when("I clear team advice")
def clear_advice(driver):
    TeamAdvicePage(driver).click_clear_advice()


@then("the give advice checkboxes are not present")
def check_advice_checkboxes_are_not_present(driver):
    driver.set_timeout_to(0)
    assert GiveAdvicePages(driver).checkbox_present() == 0
    driver.set_timeout_to_10_seconds()


@then("the give or change advice button is not present")
def check_give_advice_button_is_not_present(driver):
    driver.set_timeout_to(0)
    assert not UserAdvicePage(driver).is_advice_button_enabled()
    assert not TeamAdvicePage(driver).is_advice_button_enabled()
    assert not FinalAdvicePage(driver).is_advice_button_enabled()
    driver.set_timeout_to_10_seconds()


@then("I see total goods value")
def total_goods_value(driver, context):
    assert "Total value: £" + str(context.good_value) in Shared(driver).get_text_of_body()


@then("I dont see clearance level")
def dont_see_clearance_level(driver):
    driver.set_timeout_to(0)
    assert (
        len(GiveAdvicePages(driver).clearance_grading_present()) == 0
    ), "clearance level is displayed when it shouldn't be"
    driver.set_timeout_to_10_seconds()


@when(parsers.parse('I select "{clearance_level}" clearance level'))
def select_clearance_level(driver, clearance_level):
    GiveAdvicePages(driver).select_clearance_grading(clearance_level)


@when("I go to grouped view")
def go_to_grouped_view(driver):
    BaseAdvicePage(driver).click_grouped_view_button()


@when(parsers.parse('I select all items in the "{group}" grouped view'))
def select_all_items_in_group(driver, group):
    UserAdvicePage(driver).click_grouped_view_checkboxes(group)


@when("I click give advice")
def click_give_advice(driver):
    UserAdvicePage(driver).click_give_advice()
