import textwrap
from datetime import datetime, timedelta

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

FOREIGN_TRADER_ADDR_LINE_MAX_LEN = 35
FOREIGN_TRADER_NUM_ADDR_LINES = 5
def create_hmrc_formatted_address(addr_line):
    addr_line = addr_line.replace("\n", " ").replace("\r", " ")
    addr_lines = textwrap.wrap(addr_line, width=FOREIGN_TRADER_ADDR_LINE_MAX_LEN, break_long_words=False)
    if len(addr_lines) > FOREIGN_TRADER_NUM_ADDR_LINES:
        addr_lines = addr_lines[:FOREIGN_TRADER_NUM_ADDR_LINES]
    lines = {}
    for index, line in enumerate(addr_lines, start=1):
        lines[index] = line
    hmrc_formatted = f"{lines[1]}\\{lines.get(2,'')}\\{lines.get(3,'')}\\{lines.get(4,'')}\\{lines.get(5,'')}\\"
    return hmrc_formatted


@then("I confirm a license has been sent to HMRC")
def confirm_license_has_been_sent(context):
    body = get_smtp_body().replace("\r", "")
    ymdhm_timestamp = body.split("\n")[0].split("\\")[5]
    run_number = body.split("\n")[0].split("\\")[6]
    good_name = context.goods[0]['good']['name']
    now = datetime.now()
    today_ymd = now.strftime("%Y%m%d")
    two_years_time_ymd = (now + timedelta(days=730)).strftime("%Y%m%d")
    reference_code = context.reference_code
    reference_code_part = "".join(context.reference_code.split("/")[1:])
    end_user_name = context.end_user['name']
    end_user_address = create_hmrc_formatted_address(context.end_user['address'])
    expected_mail_body = fr"""1\fileHeader\SPIRE\CHIEF\licenceData\{ymdhm_timestamp}\{run_number}\N
2\licence\{reference_code_part}\insert\{reference_code}\SIE\E\{today_ymd}\{two_years_time_ymd}
3\trader\\1234567890AAA\{today_ymd}\{two_years_time_ymd}\Archway Communications\Headquarters\42 Question Road\\London\Greater London\SW1A 0AA
4\country\GB\\D
5\foreignTrader\{end_user_name}\{end_user_address}\GB
6\restrictions\Provisos may apply please see licence
7\line\1\\\\\{good_name}\Q\\057\\1234.0\\\\\\
8\end\licence\7
9\fileTrailer\1"""
    print(body)
    assert body.replace("\r", "") == expected_mail_body  # nosec
