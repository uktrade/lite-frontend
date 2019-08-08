from pytest import fixture
import helpers.helpers as utils
from pages.queues_pages import QueuesPages
from pages.shared import Shared


@fixture(scope="session")
def add_queue(driver, request, api_url, context):
    QueuesPages(driver).click_add_a_queue_button()
    extra_string = str(utils.get_formatted_date_time_d_h_m_s())
    context.queue_name = "Review" + extra_string
    QueuesPages(driver).enter_queue_name(context.queue_name)
    Shared(driver).click_submit()
