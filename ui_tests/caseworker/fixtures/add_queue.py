from uuid import uuid4

from pytest import fixture
from ui_tests.caseworker.pages.queues_pages import QueuesPages
from ui_tests.caseworker.pages.shared import Shared


@fixture(scope="module")
def add_queue(driver, request, api_url, context):
    QueuesPages(driver).click_add_a_queue_button()
    context.queue_name = f"Review {uuid4()}"[:25]
    QueuesPages(driver).enter_queue_name(context.queue_name)
    Shared(driver).click_submit()
