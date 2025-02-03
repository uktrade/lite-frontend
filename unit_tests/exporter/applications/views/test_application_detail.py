import pytest

from bs4 import BeautifulSoup
from django.urls import reverse

from core import client


@pytest.fixture
def mock_application_history_with_draft(requests_mock, application_history):
    application_history["amendment_history"][0]["status"] = {"status": "draft", "status_display": "draft"}
    application_history["amendment_history"][0]["submitted_at"] = None
    application_history["amendment_history"][0]["reference_code"] = None
    url = client._build_absolute_uri(f'/exporter/applications/{application_history["id"]}/history')
    return requests_mock.get(url=url, json=application_history)


@pytest.mark.parametrize(
    "can_invoke_major_editable",
    [True, False],
)
def test_edit_button(
    authorized_client,
    data_standard_case,
    mock_application_get,
    mock_application_history_get,
    mock_status_properties,
    can_invoke_major_editable,
):

    pk = data_standard_case["case"]["id"]
    mock_status_properties["can_invoke_major_editable"] = can_invoke_major_editable

    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)
    soup = BeautifulSoup(response.content, "html.parser")

    found_button = soup.find(id="button-edit-application") is not None
    assert found_button is can_invoke_major_editable


def test_appeal_refusal_decision_button(
    authorized_client,
    data_standard_case,
    mock_refused_application_get,
    mock_application_history_get,
    mock_status_properties,
):
    pk = data_standard_case["case"]["id"]

    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert bool(soup.find(id="button-appeal-refusal"))


def test_appeal_button_not_shown_for_successful_application(
    authorized_client,
    data_standard_case,
    mock_application_get,
    mock_application_history_get,
):
    pk = data_standard_case["case"]["id"]

    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert not soup.find(id="button-appeal-refusal")


@pytest.mark.parametrize(
    "date_string",
    (
        "2023-11-01T13:16:05.918259Z",
        "2023-10-04T17:12:51.271415",
        "2023-10-04T16:14:19.907345+00:00",
    ),
)
def test_appeal_deadline_date_format(
    authorized_client,
    data_standard_case,
    mock_application_get,
    mock_application_history_get,
    date_string,
):
    data_standard_case["case"]["data"]["status"] = {
        "key": "finalised",
        "value": "Finalised",
    }
    data_standard_case["case"]["data"]["appeal_deadline"] = date_string

    pk = data_standard_case["case"]["id"]

    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)

    assert response.status_code == 200


def test_user_id_hidden_field(
    authorized_client,
    data_standard_case,
    mock_application_get,
    mock_application_history_get,
    mock_exporter_user,
):
    pk = data_standard_case["case"]["id"]
    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="user_id")["value"] == mock_exporter_user["user"]["lite_api_user_id"]


def test_application_history_details(
    authorized_client,
    data_standard_case,
    mock_application_get,
    mock_application_history_get,
    mock_exporter_user,
    beautiful_soup,
):
    pk = data_standard_case["case"]["id"]
    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)
    soup = beautiful_soup(response.content)

    application_history_table = soup.find("table", attrs={"id": "table-application-history"})
    body = application_history_table.find("tbody")

    hist_application_1 = body.find_all("tr")[0].find_all("td")
    hist_application_2 = body.find_all("tr")[1].find_all("td")

    assert hist_application_1[0].text.strip() == "GBSIEL/2020/0002687/T"
    assert hist_application_1[1].text.strip() == "4:57pm 01 October 2020"
    assert hist_application_1[2].text.strip() == "Submitted"
    assert hist_application_1[3].text.strip() == ""

    assert hist_application_2[0].a["href"] == "/applications/caba228c-b4c8-41ea-804a-c1bc6ba816c7/"
    assert hist_application_2[0].a.text.strip() == "GBSIEL/2025/0000333/T"

    assert hist_application_2[1].text.strip() == "4:36pm 27 January 2025"
    assert hist_application_2[2].text.strip() == "Superseded by exporter edit"
    assert hist_application_2[3].a["href"] == "/applications/caba228c-b4c8-41ea-804a-c1bc6ba816c7/ecju-queries/"
    assert hist_application_2[3].a.text.strip() == "3"


def test_application_history_detail_with_draft(
    authorized_client,
    data_standard_case,
    mock_application_get,
    mock_application_history_with_draft,
    mock_exporter_user,
    beautiful_soup,
):
    pk = data_standard_case["case"]["id"]
    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)
    soup = beautiful_soup(response.content)

    application_history_table = soup.find("table", attrs={"id": "table-application-history"})
    body = application_history_table.find("tbody")

    hist_application_1 = body.find_all("tr")[0].find_all("td")
    hist_application_2 = body.find_all("tr")[1].find_all("td")

    assert hist_application_1[0].a.text == "Draft"
    assert hist_application_1[0].a["href"] == "/applications/8fb76bed-fd45-4293-95b8-eda9468aa254/task-list/"
    assert hist_application_1[1].text == ""
    assert hist_application_1[2].text.strip() == "draft"
    assert hist_application_1[3].text.strip() == ""

    assert hist_application_2[0].a["href"] == "/applications/caba228c-b4c8-41ea-804a-c1bc6ba816c7/"
    assert hist_application_2[0].a.text.strip() == "GBSIEL/2025/0000333/T"

    assert hist_application_2[1].text.strip() == "4:36pm 27 January 2025"
    assert hist_application_2[2].text.strip() == "Superseded by exporter edit"
    assert hist_application_2[3].a["href"] == "/applications/caba228c-b4c8-41ea-804a-c1bc6ba816c7/ecju-queries/"
    assert hist_application_2[3].a.text.strip() == "3"
