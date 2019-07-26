from pytest import fixture
import helpers.helpers as utils
from pages.add_goods_page import AddGoodPage
from pages.exporter_hub_page import ExporterHubPage


@fixture(scope="session")
def add_a_good(driver, request):
    exporter_hub = ExporterHubPage(driver)
    exporter_hub.click_my_goods()
    add_goods_page = AddGoodPage(driver)
    add_goods_page.click_add_a_good()

    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    add_goods_page.enter_description_of_goods("Widget")
    add_goods_page.select_is_your_good_controlled("Yes")
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product("no")
    add_goods_page.enter_control_code("1234")
    exporter_hub.click_save_and_continue()
    driver.get(request.config.getoption("--exporter_url"))