from pages.application_goods_list import ApplicationGoodsList
from pages.application_overview_page import ApplicationOverviewPage
from pytest import fixture

import shared.tools.helpers as utils
from shared import functions
from shared.tools.utils import get_lite_client


def add_good_to_application(driver, context, lite_client):
    url = driver.current_url
    overview_page = ApplicationOverviewPage(driver)
    context.goods_name = lite_client.context["goods_name"]
    driver.get(url)
    overview_page.click_standard_goods_link()
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()
    elements = driver.find_elements_by_css_selector(".govuk-table__row")
    no = utils.get_element_index_by_text(elements, context.goods_name, complete_match=False)
    driver.find_elements_by_css_selector(".govuk-table__row .govuk-link")[no - 1].click()
    application_goods_list = ApplicationGoodsList(driver)
    context.unit = "Number of articles"
    context.value = "11"
    application_goods_list.add_values_to_good(str(context.value), str(context.value), context.unit)
    functions.click_submit(driver)
    driver.get(url)


@fixture(scope="function")
def add_an_incorporated_good_to_application(driver, request, context, exporter_url, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_good.add_good_end_product("good_end_product_false")
    add_good_to_application(driver, context, lite_client)


@fixture(scope="function")
def add_a_non_incorporated_good_to_application(driver, context, request, exporter_url, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_good.add_good_end_product("good_end_product_true")
    add_good_to_application(driver, context, lite_client)


@fixture(scope="function")
def create_non_incorporated_good(driver, request, context, seed_data_config):
    good_name = "Modifiable Good " + utils.get_formatted_date_time_m_d_h_s()
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    good = {
        "description": good_name,
        "is_good_controlled": "yes",
        "control_code": "ML1a",
        "is_good_end_product": False,
        "part_number": "1234",
        "validate_only": False,
    }
    lite_client.seed_good.add_good(good=good)
    context.good_id = lite_client.context["good_id"]
    lite_client.seed_good.add_good_document(context.good_id)
    context.good_document = lite_client.context["document"]
