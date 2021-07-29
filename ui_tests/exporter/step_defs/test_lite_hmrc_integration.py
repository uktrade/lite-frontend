import textwrap
from urllib.parse import quote
from datetime import datetime, timedelta

import requests
from pytest_bdd import scenarios, given, when, then

scenarios("../features/lite_hmrc_integration.feature", strict_gherkin=False)

url_root = "http://localhost:8000"


def put(url):
    requests.put(url_root + url)


def get(url):
    requests.get(url_root + url)


@given("I set all emails in lite-hmrc to reply-sent")
def set_all_emails_to_reply_sent():
    put("/mail/set-all-to-reply-sent/")


@given("I force lite-hmrc to send pending licenses now")
def send_now():
    put("/mail/send-licence-updates-to-hmrc/")


@then("I confirm a license has been sent to HMRC")
def confirm_license_has_been_sent(context):
    encoded_reference_code = quote(context.reference_code, safe="")
    license = get(f"/mail/license/?id={encoded_reference_code}")
    assert "reply_pending" == license["status"]
