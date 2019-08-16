from pytest_bdd import scenarios, when, then, parsers

from pages.attach_document_page import AttachDocumentPage
from pages.goods_list import GoodsList
from pages.exporter_hub_page import ExporterHubPage
from pages.add_goods_page import AddGoodPage

scenarios('../features/add_clc_good.feature', strict_gherkin=False)


@then('I see good in goods list')
def assert_good_is_in_list(driver, context, exporter_url):
    driver.get(exporter_url.rstrip('/') + '/goods/')
    goods_list = GoodsList(driver)
    goods_list.assert_goods_are_displayed_of_good_name(context.good_description,
                                                       context.part,
                                                       context.control_code)


@then('I see the clc query in goods list')
def assert_clc_is_in_list(driver, context, exporter_url):
    driver.get(exporter_url.rstrip('/') + '/goods/')
    goods_list = GoodsList(driver)
    goods_list.assert_clc_goods_are_displayed_of_good_name(context.good_description,
                                                           context.part,
                                                           context.control_code)


@when(parsers.parse('I edit a good to description "{description}" controlled "{controlled}" '
                    'control code "{control_code}" incorporated "{incorporated}" and part number "{part}"'))
def edit_good(driver, description, controlled,  control_code, incorporated, part, context):
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    goods_list = GoodsList(driver)
    goods_list.click_on_goods_edit_link(0)
    context.edited_description = context.good_description + " " + description
    add_goods_page.enter_description_of_goods(context.edited_description)
    exporter_hub.click_save_and_continue()


@then('I see my edited good in the goods list')
def see_my_edited_good_in_list(driver, context):
    assert context.edited_description in driver.find_element_by_tag_name('body').text


@when('I delete my good')
def delete_my_good_in_list(driver, context):
    """
    Delete the recently edited good
    """
    goods_list = GoodsList(driver)

    driver.find_element_by_id('delete-' + str(context.good_id_from_url)).click()
    goods_list.click_on_delete_good_button()


@then('my good is no longer in the goods list')
def good_is_no_longer_in_list(driver, context):
    """
    Assert that the edited good is no longer in the goods list
    """
    assert len(driver.find_elements_by_id('delete-' + context.good_id_from_url)) == 0


@when('I add a good and attach a document')
def attach_document_to_modifiable_good(driver, context, create_non_incorporated_good):
    pass


@then('I see the document has been attached')
def i_see_the_attached_good(driver, context):
    added_doc = AttachDocumentPage(driver).get_text_of_document_added_item()
    assert context.file_to_be_deleted_name in added_doc, "file is not displayed"
    assert context.document_description in added_doc, "file description is not displayed"
