from urllib.parse import quote
import pytest

from pytest_bdd import scenarios, given, then

from tests_common.api_client.lite_hmrc_client import ApiClient

scenarios("../features/lite_hmrc_integration.feature", strict_gherkin=False)


@pytest.fixture
def hmrc_lite_api_client():
    return ApiClient()


@given("I set all emails in lite-hmrc to reply-sent")
def set_all_emails_to_reply_sent(hmrc_lite_api_client):
    hmrc_lite_api_client.make_request("GET", "/mail/set-all-to-reply-sent/")


@given("I force lite-hmrc to send pending licences now")
def send_now(hmrc_lite_api_client):
    hmrc_lite_api_client.make_request("GET", "/mail/send-licence-updates-to-hmrc/")


@then("I confirm a licence has been sent to HMRC")
def confirm_licence_has_been_sent(context, hmrc_lite_api_client):
    encoded_reference_code = quote(context.reference_code, safe="")
    response = hmrc_lite_api_client.make_request("GET", f"/mail/licence/?id={encoded_reference_code}")
    assert "reply_pending" == response.json()["status"]
