import time

from pytest_bdd import when, then, parsers
from selenium.webdriver.common.by import By

from tests_common import functions
from ui_tests.caseworker.pages.assign_flags_to_case import CaseFlagsPages
from ui_tests.caseworker.pages.shared import Shared
from ui_tests.caseworker.pages.advice import RecommendationsAndDecisionPage
from ui_tests.caseworker.pages.case_page import CasePage, CaseTabs
from ui_tests.caseworker.pages.generate_decision_documents_page import GeneratedDecisionDocuments
from ui_tests.caseworker.pages.generate_document_page import GeneratedDocument
from ui_tests.caseworker.pages.give_advice_pages import GiveAdvicePages
from ui_tests.caseworker.pages.application_page import ApplicationPage


@when("I click the recommendations and decision tab")
def click_on_recommendations_and_decision_tab(driver):
    CasePage(driver).change_tab("advice")


@when("I click make recommendation")
def click_make_recommendation_button(driver):  # noqa
    RecommendationsAndDecisionPage(driver).click_make_recommendation()


@when("I click refuse")
def click_refuse(driver):  # noqa
    RecommendationsAndDecisionPage(driver).click_refuse()


@when("I click approve all")
def click_approve_all(driver):  # noqa
    RecommendationsAndDecisionPage(driver).click_approve_all()


@when("I click refuse all")
def click_refuse_all(driver):  # noqa
    RecommendationsAndDecisionPage(driver).click_refuse_all()


@when(parsers.parse('I select refusal criteria "{criteria}"'))
def select_refusal_criteria(driver, criteria):  # noqa
    functions.select_multi_select_options(
        driver,
        "#div_id_denial_reasons .lite-autocomplete__input",
        [c.strip() for c in criteria.split(",")],
    )


@when(parsers.parse('I select countries "{countries}"'))
def select_countries(driver, countries):  # noqa
    page = RecommendationsAndDecisionPage(driver)

    for country in countries.split(","):
        page.select_country(country.strip())


@when(parsers.parse('I enter "{reasons}" as the overall reason'))
@when(parsers.parse('I enter "{reasons}" as the reasons for approving'))
def enter_reasons_for_approving(driver, reasons, context):  # noqa
    RecommendationsAndDecisionPage(driver).enter_reasons_for_approving(reasons)


@when(parsers.parse('I enter "{reasons}" as the reasons for refusal'))
def enter_reasons_for_refusal(driver, reasons, context):  # noqa
    RecommendationsAndDecisionPage(driver).enter_reasons_for_refusal(reasons)


@when(parsers.parse('I enter "{note}" as refusal meeting note'))
def enter_refusal_note(driver, note, context):  # noqa
    RecommendationsAndDecisionPage(driver).enter_refusal_note(note)


@when(parsers.parse('I enter "{licence_condition}" as the licence condition'))
def enter_licence_condition(driver, licence_condition, context):  # noqa
    RecommendationsAndDecisionPage(driver).enter_licence_condition(licence_condition)


@when(parsers.parse('I enter "{instructions}" as the instructions for the exporter'))
def enter_instructions_for_exporter(driver, instructions, context):  # noqa
    RecommendationsAndDecisionPage(driver).enter_instructions_for_exporter(instructions)


@when(parsers.parse('I enter "{footnote}" as the reporting footnote'))
def enter_reporting_footnote(driver, footnote, context):  # noqa
    RecommendationsAndDecisionPage(driver).enter_reporting_footnote(footnote)


@then(parsers.parse('I should see my recommendation for "{countries}" with "{reasons}"'))
def should_see_recommendation(driver, countries, reasons):  # noqa
    text = driver.find_element(by=By.XPATH, value="//main[@class='govuk-main-wrapper']//*").text
    for country in countries.split(","):
        assert country.strip() in text
    assert reasons.strip() in text


@then(parsers.parse('I see there are no recommendations from "{team}"'))
def should_not_see_recommendation(driver, team, context):  # noqa
    assert f"{team} has approved" not in Shared(driver).get_text_of_body()


@then("I am asked what my recommendation is")
def should_ask_for_recommendation(driver):  # noqa
    assert Shared(driver).get_text_of_heading().text == "What is your recommendation?"


@then(parsers.parse('I see "{reasons}" as the overall reason'))
@then(parsers.parse('I see "{reasons}" as the reasons for approving'))
def should_see_reasons_for_approving(driver, reasons, context):  # noqa
    assert RecommendationsAndDecisionPage(driver).get_reasons_for_approving() == reasons


@then(parsers.parse('I see "{reasons}" as the reasons for refusal'))
def should_see_reasons_for_refusal(driver, reasons, context):  # noqa
    assert RecommendationsAndDecisionPage(driver).get_reasons_for_refusal() == reasons


@then(parsers.parse('I see "{note}" as refusal meeting note'))
def should_see_refusal_meeting_note(driver, note, context):  # noqa
    assert RecommendationsAndDecisionPage(driver).get_refusal_note() == note


@then(parsers.parse('I see "{criteria}" as the refusal criteria'))
def should_see_refusal_criteria(driver, criteria):  # noqa
    page = RecommendationsAndDecisionPage(driver)

    assert all(crit == criteria for crit in page.get_refusal_criteria())


@then(parsers.parse('I see "{licence_condition}" as the licence condition'))
def should_see_licence_condition(driver, licence_condition, context):  # noqa
    assert RecommendationsAndDecisionPage(driver).get_licence_condition() == licence_condition


@then(parsers.parse('I see "{instructions}" as the instructions for the exporter'))
def should_see_instructions_for_exporter(driver, instructions, context):  # noqa
    assert RecommendationsAndDecisionPage(driver).get_instructions_for_exporter() == instructions


@then(parsers.parse('I see "{footnote}" as the reporting footnote'))
def should_see_reporting_footnote(driver, footnote, context):  # noqa
    assert RecommendationsAndDecisionPage(driver).get_reporting_footnote() == footnote


@then("I see the application reference on the document preview")
def should_see_application_ref_on_refusal_letter(driver, context):  # noqa
    text = GeneratedDocument(driver).get_document_preview_text()
    assert f"{context.reference_code}" in text


@then("I see the licence number on the SIEL licence preview")
def should_see_licence_number_on_siel_licence_preview(driver, context):
    element = driver.find_element(by=By.ID, value="licence-reference-column")
    expected_reference = element.find_element(by=By.XPATH, value=".//span[contains(@class, 'cell__uppercase')]").text
    assert context.reference_code == expected_reference


@then(parsers.parse('I see that "{item_name}" is "{value}" on the SIEL licence preview'))  # noqa
def should_see_item_on_siel_licence_preview(driver, item_name, value):  # noqa
    assert value == GeneratedDocument(driver).get_item_from_siel_document_preview(item_name)


@then(parsers.parse('the document name should be "{name}"'))
def should_see_document_name_in_document_list(driver, name, context):  # noqa
    doc_name = GeneratedDecisionDocuments(driver).get_decision_document_name()
    assert name == doc_name


@then("I see the product name under name on the document preview")
def should_see_product_name_on_nlr_preview(driver, context):  # noqa
    prod_name = GeneratedDocument(driver).get_product_name_from_nlr_document_preview()
    assert context.goods[0]["good"]["name"] == prod_name


@when("I go to the team advice")
def go_to_team_advice(driver):
    CasePage(driver).change_tab(CaseTabs.TEAM_ADVICE)


@when("I go to the final advice")
def go_to_final_advice(driver):
    CasePage(driver).change_tab(CaseTabs.FINAL_ADVICE)


@when(parsers.parse('I select "{clearance_level}" clearance level'))
def select_clearance_level(driver, clearance_level):
    GiveAdvicePages(driver).select_clearance_grading(clearance_level)


@when(parsers.parse('I set a "{level}" flag'))  # noqa
def assign_flags_to_case(driver, context, level):  # noqa
    CaseFlagsPages(driver).select_flag(level)
    functions.click_submit(driver)


@when(parsers.parse('I unset a "{level}" flag'))  # noqa
def assign_flags_to_case(driver, context, level):  # noqa
    CaseFlagsPages(driver).deselect_flag(level)
    functions.click_submit(driver)


@when("I click edit flags on the last destination")
def click_edit_destination_flags_link(driver):
    destinations = CasePage(driver).get_destinations()
    case_page = CasePage(driver)
    case_page.select_destination(len(destinations) - 1)
    case_page.click_edit_destinations_flags()


@when("I click on details")
def click_on_link(driver):
    Shared(driver).expand_govuk_details()
    time.sleep(1)


@when(parsers.parse('I enter "{text}" as the countersign note'))
def enter_case_note_text(driver, text, context):
    application_page = ApplicationPage(driver)
    if text == "too many characters":
        text = "T" * 2201
    context.text = text
    application_page.enter_countersign_note(text)


@then(parsers.parse('I see the case is assigned to "{queue}"'))  # noqa
def case_not_assigned_to_any_queue(driver, queue):  # noqa
    assert CasePage(driver).get_assigned_queues() == queue


@then("I see countersign required warning message")
def lu_countersign_warning_message(driver):  # noqa
    countersign_warning_message = (
        "This case requires countersigning. Moving this case on will pass it to the countersigning work queue."
    )
    assert countersign_warning_message in RecommendationsAndDecisionPage(driver).get_lu_countersign_warning_message()


@when(parsers.parse('I agree with outcome and provide "{comments}" as countersign comments'))  # noqa
def agree_with_outcome(driver, comments):  # noqa
    RecommendationsAndDecisionPage(driver).agree_with_outcome_and_countersign(comments)


@when(parsers.parse('I disagree with outcome and provide "{comments}" as countersign comments'))  # noqa
def disagree_with_outcome(driver, comments):  # noqa
    RecommendationsAndDecisionPage(driver).disagree_with_outcome_and_countersign(comments)


@then(parsers.parse('I see "{comments}" as countersign comments'))
def check_countersign_comments(driver, comments):  # noqa
    assert RecommendationsAndDecisionPage(driver).get_countersign_comments() == comments


@then(parsers.parse('I see "{inform_letter}" in decision documents'))
def see_inform_letter(driver, inform_letter):
    elements = driver.find_elements(By.CSS_SELECTOR, "td.govuk-table__cell")
    matching_elements = [e for e in elements if inform_letter in e.text]

    assert matching_elements[0]


@when(parsers.parse('I click "{inform_letter_button}" button'))
def create_inform_letter(driver, inform_letter_button):
    if inform_letter_button == "Create Inform letter" or inform_letter_button == "Recreate":
        id = "generate-document-inform"
        driver.find_element(By.ID, id).click()
    if inform_letter_button == "Send inform letter":
        row = driver.find_element(By.CSS_SELECTOR, "tr#decision-inform")
        button = row.find_element(By.CSS_SELECTOR, "button")
        if button.text == "Send inform letter":
            button.click()


@when(parsers.parse('I select "{template}" radio button'))
def select_template_radio(driver, template):
    labels = driver.find_elements(By.CSS_SELECTOR, "label.govuk-label")
    for label in labels:
        if template in label.text:
            input_id = label.get_attribute("for")
            driver.find_element(By.ID, input_id).click()
            break


@then(parsers.parse('I see "{status}" inform letter status in decision documents'))
def check_status(driver, status):
    element = driver.find_element(By.ID, "status-inform")
    assert element.text == status


@when(parsers.parse("I click inform letter edit link"))
def click_edit_inform_letter(driver):
    row = driver.find_element(By.CSS_SELECTOR, "tr#decision-inform")
    row.find_element(By.CSS_SELECTOR, "a[href*='edit-letter/inform']").click()


@when(parsers.parse('I edit template with "{text}"'))
def edit_template(driver, text):
    textarea = driver.find_element(By.ID, "id_text")
    textarea.clear()
    textarea.send_keys(text)


@then(parsers.parse('I see the "{content}" text on the document preview'))
def should_see_content_on_inform_letter(driver, content):
    text = GeneratedDocument(driver).get_document_preview_text()
    assert content in text


@then("I see warning that case cannot be finalised due to a query that needs to be closed")
def i_see_warning_about_open_query(driver):
    warning_element = driver.find_element(by=By.ID, value="case-has-open-queries")
    assert "Warning" in warning_element.text
    assert "This case cannot be finalised due to a query that needs to be closed." in warning_element.text

    action_items = [item.text for item in driver.find_elements(by=By.CLASS_NAME, value="govuk-button")]
    assert "Finalise case" not in action_items


@then("I see countersign not allowed warning message")
def lu_countersign_not_allowed_warning_message(driver):  # noqa
    countersign_warning_message = "You cannot countersign this case because you were the officer that assessed it."
    assert (
        countersign_warning_message
        in RecommendationsAndDecisionPage(driver).get_lu_countersign_not_allowed_warning_message()
    )
