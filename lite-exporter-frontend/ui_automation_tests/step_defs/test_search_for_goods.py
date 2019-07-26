from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.application_goods_list import ApplicationGoodsList

scenarios('../features/search_for_goods.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I filter by description and click filter')
def filter_by_description(driver, context):
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.type_into_filter_description_search_box_and_filter(context.good_description)


@when('I filter by part number and click filter')
def filter_by_part_no(driver, context):
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.type_into_filter_part_number_search_box_and_filter(context.part)


@when('I remove the filters')
def remove_filters(driver, context):
    application_goods_list = ApplicationGoodsList(driver)
    application_goods_list.remove_filters()


@then(parsers.parse('I see my added good by "{type}"'))
def see_added_good(driver, type, context):
    application_goods_list = ApplicationGoodsList(driver)
    assert application_goods_list.get_size_of_goods() == 1
    if type == 'description':
        assert application_goods_list.get_tag_name_of_good(0) == context.good_description
    elif type == 'part number':
        assert context.part in application_goods_list.get_text_of_good(0)


@then('I see all goods')
def remove_filters(driver):
    application_goods_list = ApplicationGoodsList(driver)
    assert application_goods_list.get_size_of_goods() > 1
