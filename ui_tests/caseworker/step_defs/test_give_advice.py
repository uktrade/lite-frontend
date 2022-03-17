from pytest_bdd import when, then, parsers, scenarios

from ui_tests.caseworker.pages.shared import Shared
from ui_tests.caseworker.pages.advice import RecommendationsAndDecisionPage
from ui_tests.caseworker.pages.case_page import CasePage, CaseTabs
from ui_tests.caseworker.pages.generate_document_page import GeneratedDocument
from ui_tests.caseworker.pages.give_advice_pages import GiveAdvicePages

scenarios("../features/give_advice.feature", strict_gherkin=False)


@when("I click move case forward")
@when("I click submit recommendation")
@when("I click save and publish to exporter")
def submit_form(driver):  # noqa
    Shared(driver).click_submit()


@when("I click the recommendations and decision tab")
def click_on_recommendations_and_decision_tab(driver, context):  # noqa
    CasePage(driver).change_tab("advice")


@when("I click make recommendation")
def click_make_recommendation_button(driver):  # noqa
    RecommendationsAndDecisionPage(driver).click_make_recommendation()


@when("I click approve all")
def click_approve_all(driver):  # noqa
    RecommendationsAndDecisionPage(driver).click_approve_all()


@when("I click refuse all")
def click_refuse_all(driver):  # noqa
    RecommendationsAndDecisionPage(driver).click_refuse_all()


@when(parsers.parse('I select refusal criteria "{criteria}"'))
def select_refusal_criteria(driver, criteria):  # noqa
    page = RecommendationsAndDecisionPage(driver)

    for crit in criteria.split(","):
        page.select_refusal_criteria(crit.strip())


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
    text = driver.find_element_by_xpath("//main[@class='govuk-main-wrapper']//*").text
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


@then("I see the licence number on the SIEL licence preview")
def should_see_licence_number_on_siel_licence_preview(driver, context):  # noqa
    text = GeneratedDocument(driver).get_document_preview_text()
    assert f"{context.reference_code}-01" in text


@then(parsers.parse('I see that "{item_name}" is "{value}" on the SIEL licence preview'))  # noqa
def should_see_item_on_siel_licence_preview(driver, item_name, value):  # noqa
    assert value == GeneratedDocument(driver).get_item_from_siel_document_preview(item_name)


@when("I go to the team advice")
def go_to_team_advice(driver):
    CasePage(driver).change_tab(CaseTabs.TEAM_ADVICE)


@when("I go to the final advice")
def go_to_final_advice(driver):
    CasePage(driver).change_tab(CaseTabs.FINAL_ADVICE)


@when(parsers.parse('I select "{clearance_level}" clearance level'))
def select_clearance_level(driver, clearance_level):
    GiveAdvicePages(driver).select_clearance_grading(clearance_level)
