from pytest import fixture
import shared.tools.helpers as utils
from pages.flags_pages import FlagsPages
from pages.shared import Shared


@fixture(scope="session")
def add_uae_flag(driver, context):
    flags_page = FlagsPages(driver)
    flags_page.click_add_a_flag_button()
    extra_string = str(utils.get_formatted_date_time_d_h_m_s())
    context.flag_name = "UAE" + extra_string
    flags_page.enter_flag_name(context.flag_name)
    flags_page.select_flag_level("Case")
    Shared(driver).click_submit()
    assert context.flag_name in Shared(driver).get_text_of_table()


@fixture(scope="session")
def add_suspicious_flag(driver, context):
    flags_page = FlagsPages(driver)
    flags_page.click_add_a_flag_button()
    extra_string = str(utils.get_formatted_date_time_d_h_m_s())
    context.flag_name = "Suspicious" + extra_string
    flags_page.enter_flag_name(context.flag_name)
    flags_page.select_flag_level("Good")
    Shared(driver).click_submit()
    assert context.flag_name in Shared(driver).get_text_of_table()
