from datetime import date

from pytest_bdd import when, then, parsers, scenarios

from pages.advice import UserAdvicePage, FinalAdvicePage, TeamAdvicePage, BaseAdvicePage
from pages.case_page import CasePage, CaseTabs
from pages.give_advice_pages import GiveAdvicePages
from pages.record_decision_page import RecordDecision
from pages.shared import Shared
from ui_automation_tests.pages.grant_licence_page import GrantLicencePage

scenarios("../features/give_advice.feature", strict_gherkin=False)


@when(parsers.parse('I select decision "{number}"'))
def select_decision(driver, number, context):
    record = RecordDecision(driver)
    record.click_on_decision_number(number)
    context.advice_data.append(number)


@when("I select all items in the team advice view")
def click_items_in_advice_view(driver, context):
    context.number_of_advice_items_clicked = TeamAdvicePage(driver).click_on_all_checkboxes()


@when(parsers.parse("I select that a footnote is required with the note '{text}'"))
def write_note_text_field(driver, text, context):
    give_advice_page = GiveAdvicePages(driver)
    give_advice_page.select_footnote_required()
    give_advice_page.enter_footnote(text)
    context.advice_data.append(text)


@then("I see the fields pre-populated with the proviso and advice picklist items")
def i_see_fields_prepopulated(driver, context):
    text = driver.find_element_by_id("text").text
    proviso = driver.find_element_by_id("proviso").text
    assert text == context.standard_advice_query_picklist_question_text
    assert proviso == context.proviso_picklist_question_text


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
    driver.implicitly_wait(0)
    assert GiveAdvicePages(driver).checkbox_present() == 0
    driver.implicitly_wait(10)


@then("the give or change advice button is not present")
def check_give_advice_button_is_not_present(driver):
    driver.implicitly_wait(0)
    assert not UserAdvicePage(driver).is_advice_button_enabled()
    assert not TeamAdvicePage(driver).is_advice_button_enabled()
    assert not FinalAdvicePage(driver).is_advice_button_enabled()
    driver.implicitly_wait(10)


@then("I see total goods value")
def total_goods_value(driver, context):
    assert "Total value: £" + str(context.good_value) in Shared(driver).get_text_of_body()


@then("I dont see clearance level")
def dont_see_clearance_level(driver):
    driver.implicitly_wait(0)
    assert (
        len(GiveAdvicePages(driver).clearance_grading_present()) == 0
    ), "clearance level is displayed when it shouldn't be"
    driver.implicitly_wait(10)


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
