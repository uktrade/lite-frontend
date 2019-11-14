import os

from pytest import fixture

from shared import functions
import shared.tools.helpers as utils
from pages.add_goods_page import AddGoodPage
from pages.application_goods_list import ApplicationGoodsList
from pages.application_overview_page import ApplicationOverviewPage
from pages.attach_document_page import AttachDocumentPage
from pages.exporter_hub_page import ExporterHubPage
from shared.tools.utils import get_lite_client


def add_good_to_application(driver, context, lite_client):
    url = driver.current_url
    overview_page = ApplicationOverviewPage(driver)
    context.goods_name = lite_client.context['goods_name']
    driver.get(url)
    overview_page.click_standard_goods_link()
    driver.find_element_by_css_selector('a[href*="add-preexisting"]').click()
    elements = driver.find_elements_by_css_selector('.govuk-table__row')
    no = utils.get_element_index_by_text(elements, context.goods_name, complete_match=False)
    driver.find_elements_by_css_selector('.govuk-table__row .govuk-link')[no - 1].click()
    application_goods_list = ApplicationGoodsList(driver)
    context.unit = 'Number of articles'
    context.value = '11'
    application_goods_list.add_values_to_good(str(context.value), str(context.value), context.unit)
    functions.click_submit(driver)
    driver.get(url)


@fixture(scope="function")
def add_an_incorporated_good_to_application(driver, request, context, exporter_url, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_good.add_good_end_product('good_end_product_false')
    add_good_to_application(driver, context, lite_client)


@fixture(scope="function")
def add_a_non_incorporated_good_to_application(driver, context, request, exporter_url, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config=seed_data_config)
    lite_client.seed_good.add_good_end_product('good_end_product_true')
    add_good_to_application(driver, context, lite_client)


@fixture(scope='function')
def create_non_incorporated_good(driver, request, context):
    good_name = "Modifiable Good " + utils.get_formatted_date_time_m_d_h_s()
    context.goods_name = good_name
    exporter_hub = ExporterHubPage(driver)
    driver.get(request.config.getoption("--exporter_url"))
    exporter_hub.click_my_goods()
    add_goods_page = AddGoodPage(driver)
    add_goods_page.click_add_a_good()
    add_goods_page = AddGoodPage(driver)
    add_goods_page.enter_description_of_goods(good_name)
    add_goods_page.select_is_your_good_controlled("Yes")
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product("No")
    add_goods_page.enter_control_code("ML1a")
    functions.click_submit(driver)
    context.file_to_be_deleted_name = 'file_for_doc_upload_test_2.txt'
    # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
    file_to_upload_abs_path = \
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, 'resources', context.file_to_be_deleted_name))
    if 'ui_automation_tests' not in file_to_upload_abs_path:
        file_to_upload_abs_path = \
            os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'ui_automation_tests/resources',
                                         context.file_to_be_deleted_name))

    attach_document_page = AttachDocumentPage(driver)
    attach_document_page.choose_file(file_to_upload_abs_path)
    context.document_description = utils.get_formatted_date_time_m_d_h_s()
    attach_document_page.enter_description(context.document_description)
    functions.click_submit(driver)
