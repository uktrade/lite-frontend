from urllib.parse import quote

import requests
from pytest_bdd import scenarios, given, when, then

scenarios("../features/lite_hmrc_integration.feature", strict_gherkin=False)

lite_hmrc_root = "http://localhost:8000"


@given("I set all emails in lite-hmrc to reply-sent")
def set_all_emails_to_reply_sent():
    requests.get(lite_hmrc_root + "/mail/set-all-to-reply-sent/")


@given("I force lite-hmrc to send pending licences now")
def send_now():
    requests.get(lite_hmrc_root + "/mail/send-licence-updates-to-hmrc/")


@then("I confirm a licence has been sent to HMRC")
def confirm_licence_has_been_sent(context):
    encoded_reference_code = quote(context.reference_code, safe="")
    response = requests.get(lite_hmrc_root + f"/mail/licence/?id={encoded_reference_code}")
    assert "reply_pending" == response.json()["status"]
