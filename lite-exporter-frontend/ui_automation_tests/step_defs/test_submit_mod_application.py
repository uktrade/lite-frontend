from pytest_bdd import scenarios, when, parsers, then

from ui_automation_tests.pages.add_end_user_pages import AddEndUserPages
from ui_automation_tests.pages.exporter_hub_page import ExporterHubPage
from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.pages.apply_for_a_licence_page import ApplyForALicencePage
from ui_automation_tests.pages.mod_clearances.ExhibitionClearanceGood import ExhibitionClearanceGoodPage
from ui_automation_tests.pages.shared import Shared
from ui_automation_tests.pages.standard_application.goods import StandardApplicationGoodsPage
from ui_automation_tests.shared import functions
import ui_automation_tests.shared.tools.helpers as utils

scenarios("../features/submit_mod_application.feature", strict_gherkin=False)


@when(parsers.parse('I select a MOD licence of type "{type}"'))  # noqa
def create_mod_application(driver, context, type):  # noqa
    ApplyForALicencePage(driver).select_mod_application_type(type)
    functions.click_submit(driver)


@when("I add a good to the Exhibition Clearance")  # noqa
def i_add_a_exhibition_style_good_on_application(driver, context):  # noqa
    goods_page = StandardApplicationGoodsPage(driver)
    goods_page.click_add_preexisting_good_button()
    goods_page.click_add_to_application()

    # Enter good details
    context.good_type = "equipment"
    ExhibitionClearanceGoodPage(driver).click_good_type(context.good_type)
    functions.click_submit(driver)


@then("the good is added to the Exhibition Clearance")  # noqa
def the_good_is_added_to_the_exhibition_application(driver, context):  # noqa
    assert len(StandardApplicationGoodsPage(driver).get_goods()) == 1  # Only one good added
    assert "Equipment" in Shared(driver).get_table_row(1).text

    # Go back to task list
    functions.click_back_link(driver)


@when(parsers.parse('I select a licence of type "{type}"'))  # noqa
def create_mod_application(driver, context, type):  # noqa
    ExporterHubPage(driver).click_apply_for_a_licence()
    ApplyForALicencePage(driver).select_licence_type(type)
    functions.click_submit(driver)


@when("I choose the types of clearance I need")
def choose_types_of_clearance(driver):
    ApplyForALicencePage(driver).select_types_of_clearance()
    functions.click_submit(driver)


@then("I see the correct number of clearance types")
def correct_number_of_types(driver):
    assert len(driver.find_elements_by_name(ApplyForALicencePage(driver).F680_CLEARANCE_TYPE_CHECKBOXES_NAME)) == 6


@when(  # noqa
    parsers.parse(
        'I add an end user with clearance of sub_type: "{type}", name: "{name}", '
        'website: "{website}", clearance: "{clearance}", address: "{address}" and country "{'
        'country}"'
    )
)
def add_new_end_user_with_clearance(driver, type, name, website, clearance, address, country, context):  # noqa
    add_end_user_pages = AddEndUserPages(driver)
    add_end_user_pages.create_new_or_copy_existing(copy_existing=False)
    add_end_user_pages.select_type(type)
    context.type_end_user = type
    functions.click_submit(driver)
    add_end_user_pages.enter_name(name)
    context.name_end_user = name
    functions.click_submit(driver)
    add_end_user_pages.enter_website(website)
    functions.click_submit(driver)
    no = utils.get_element_index_by_text(Shared(driver).get_radio_buttons_elements(), clearance)
    Shared(driver).click_on_radio_buttons(no)
    functions.click_submit(driver)
    functions.click_submit(driver)
    add_end_user_pages.enter_address(address)
    context.address_end_user = address
    add_end_user_pages.enter_country(country)
    functions.click_submit(driver)
