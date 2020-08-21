from pytest import fixture
import tests_common.tools.helpers as utils
from ui_tests.caseworker.pages.queues_pages import QueuesPages
from ui_tests.caseworker.pages.shared import Shared


@fixture(scope="module")
def add_queue(driver, request, api_url, context):
    QueuesPages(driver).click_add_a_queue_button()
    context.queue_name = f"Review {utils.get_formatted_date_time_d_h_m_s()}"
    QueuesPages(driver).enter_queue_name(context.queue_name)
    Shared(driver).click_submit()
