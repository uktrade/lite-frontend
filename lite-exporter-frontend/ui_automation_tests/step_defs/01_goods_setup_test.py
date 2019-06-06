from pytest_bdd import scenarios, given, when, then, parsers
from pages.goods_list import GoodsList
from pages.exporter_hub_page import ExporterHubPage
from pages.add_goods_page import AddGoodPage
from conftest import context

scenarios('../features/add_goods.feature', strict_gherkin=False)


@then('I see good in goods list')
def assert_good_is_in_list(driver):
    goods_list = GoodsList(driver)
    goods_list.assert_goods_are_displayed_of_good_name(context.good_description, context.part, context.controlcode)
