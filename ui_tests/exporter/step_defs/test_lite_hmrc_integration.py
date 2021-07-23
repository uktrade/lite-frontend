import requests
from pytest_bdd import scenarios, given, when, then

scenarios("../features/lite_hmrc_integration.feature", strict_gherkin=False)

url_root = "http://localhost:8000"


def put(url):
    requests.put(url_root + url)


def post(url, data=None):
    requests.post(url_root + url, json=data)


def get_smtp_body():
    response = requests.get("http://localhost:8025/api/v2/messages")
    print(response)
    return response.json()["items"][0]["MIME"]["Parts"][1]["Body"]


@given("I clear the HMRC mailbox")
def clear_mailbox():
    response = requests.get("http://localhost:8025/api/v2/messages")
    print(response)
    for message in response.json()["items"]:
        id = message["ID"]
        requests.delete(f"http://localhost:8025/api/v1/messages/{id}")


@given("I set all emails in lite-hmrc to reply-sent")
def set_all_emails_to_reply_sent():
    put("/mail/set-all-to-reply-sent/")


@given("I force lite-hmrc to send pending licenses now")
def send_now():
    put("/mail/send-licence-updates-to-hmrc/")


expected_mail_body = r"""3\trader\\1234567890AAA\20210723\20230723\Archway Communications\Headquarters\42 Question Road\\London\Greater London\SW1A 0AA
4\country\GB\\D
5\foreignTrader\Steven Juarez\08199 Amy Estates Suite 975, Texas,\75694\\\\\GB
6\restrictions\Provisos may apply please see licence
7\line\1\\\\\Rifle\Q\\057\\1234.0\\\\\\
8\end\licence\7
9\fileTrailer\1
"""


@then("I confirm a license has been sent to HMRC")
def confirm_license_has_been_sent():
    body = get_smtp_body().replace("\r", "")
    # Remove the first and second line as it contains data that changes every time
    body = "\n".join(body.split("\n")[2:])
    print(body)
    assert body.replace("\r", "") == expected_mail_body  # nosec
