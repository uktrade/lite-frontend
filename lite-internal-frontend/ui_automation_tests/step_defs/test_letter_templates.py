import uuid

from pytest_bdd import scenarios, when, then, given
import shared.tools.helpers as utils

from pages.header_page import HeaderPage
from pages.letter_templates import LetterTemplates
from pages.shared import Shared
from ui_automation_tests.fixtures.add_a_document_template import get_paragraph_text

scenarios("../features/letter_templates.feature", strict_gherkin=False)


@given("I create a letter paragraph picklist")
def add_letter_paragraph_picklist(add_a_letter_paragraph_picklist):
    pass


@when("I go to letters")
def go_to_letters(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_letters()


@when("I create a letter template")
def create_letter_template(driver, context, get_template_id):
    LetterTemplates(driver).click_create_a_template()
    context.template_name = "Template " + utils.get_formatted_date_time_m_d_h_s()
    LetterTemplates(driver).enter_template_name(context.template_name)
    Shared(driver).click_submit()
    LetterTemplates(driver).select_which_type_of_case_template_can_apply_to("Applications")
    Shared(driver).click_submit()
    LetterTemplates(driver).click_licence_layout(get_template_id)
    Shared(driver).click_submit()


@when("I add a letter paragraph to template")
def add_two_letter_paragraphs(driver, context):
    letter_template = LetterTemplates(driver)
    letter_template.click_add_letter_paragraph()
    context.letter_paragraph_name = letter_template.add_letter_paragraph()
    letter_template.click_add_letter_paragraphs()


@when("I preview template")
def preview_template(driver):
    LetterTemplates(driver).click_create_preview_button()


@then("my picklist is in template")
def picklist_in_template(driver, context):
    assert context.picklist_text in LetterTemplates(driver).get_text_of_paragraphs_in_template()


@when("I click save")
def click_save(driver):
    Shared(driver).click_submit()


@then("I see my template in the table")
def templates_in_table(driver, context):
    assert context.template_name in Shared(driver).get_text_of_table()


@when("I edit my template")
def edit_template(driver, context):
    driver.find_element_by_link_text(context.template_name).click()
    LetterTemplates(driver).click_edit_details_button()
    context.template_name = context.template_name + " edited"
    LetterTemplates(driver).enter_template_name(context.template_name)
    Shared(driver).click_submit()
    Shared(driver).click_back()


@then("I see the drag and drop page")
def see_drag_and_drop_page(driver, context):
    letter_template = LetterTemplates(driver)
    context.picklist_text = letter_template.get_text_of_paragraphs_in_preview()
    assert "app-sortable ui-sortable" in letter_template.get_class_name_of_drag_and_drop_list()
    assert context.letter_paragraph_name in letter_template.get_drag_and_drop_list_name()


@given("I create a document template")
def create_a_document_template(add_a_document_template):
    pass


@when("I click on my template")
def click_on_my_template(driver, context):
    LetterTemplates(driver).click_letter_template(context.document_template_name)


@then("The template details are present")
def template_details_are_present(driver, context):
    letter_template = LetterTemplates(driver)
    assert context.document_template_name == letter_template.get_template_title()
    assert context.document_template_layout == letter_template.get_template_layout()

    for case_type in context.document_template_restricted_to:
        assert case_type in letter_template.get_template_restricted_to()


@then("The paragraph text is present")
def paragraph_text_is_present(driver, context):
    letter_paragraphs = LetterTemplates(driver).get_template_paragraphs()
    for paragraph in context.document_template_paragraph_text:
        assert paragraph in letter_paragraphs


@when("I edit my template name and layout")
def edit_template_name_and_layout(driver, context):
    context.document_template_name = str(uuid.uuid4())[:35]
    context.document_template_restricted_to.append("CLC Query")
    letter_template = LetterTemplates(driver)
    letter_template.click_edit_template_button()
    letter_template.enter_template_name(context.document_template_name)
    letter_template.select_which_type_of_case_template_can_apply_to("CLC Query")
    Shared(driver).click_submit()


@when("I edit my template paragraphs")
def edit_template_paragraphs(driver, context, seed_data_config):
    letter_template = LetterTemplates(driver)
    letter_template.click_edit_paragraphs_button()
    letter_template.click_add_paragraph_link()
    paragraph_id = letter_template.get_add_paragraph_button()
    context.document_template_paragraph_text.append(get_paragraph_text(context, seed_data_config, paragraph_id))
    Shared(driver).click_submit()


@then("The template paragraphs have been edited")
def template_paragraphs_have_been_edited(driver, context):
    paragraphs_text_list = LetterTemplates(driver).get_list_of_letter_paragraphs()
    for text in context.document_template_paragraph_text:
        assert text in paragraphs_text_list
