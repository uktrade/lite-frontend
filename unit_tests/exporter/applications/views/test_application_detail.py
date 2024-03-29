import pytest

from bs4 import BeautifulSoup
from django.urls import reverse


@pytest.mark.parametrize(
    "is_read_only",
    [True, False],
)
def test_edit_button(authorized_client, data_standard_case, mock_application_get, mock_status_properties, is_read_only):
    pk = data_standard_case["case"]["id"]
    mock_status_properties["is_read_only"] = is_read_only

    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)
    soup = BeautifulSoup(response.content, "html.parser")
    if is_read_only:
        assert not soup.find(id="button-edit-application")
    else:
        assert soup.find(id="button-edit-application")


def test_appeal_refusal_decision_button(authorized_client, data_standard_case, mock_refused_application_get):
    pk = data_standard_case["case"]["id"]

    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert bool(soup.find(id="button-appeal-refusal"))


def test_appeal_button_not_shown_for_successful_application(
    authorized_client, data_standard_case, mock_application_get
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


def test_user_id_hidden_field(authorized_client, data_standard_case, mock_application_get, mock_exporter_user):
    pk = data_standard_case["case"]["id"]
    application_url = reverse("applications:application", kwargs={"pk": pk})
    response = authorized_client.get(application_url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find(id="user_id")["value"] == mock_exporter_user["user"]["lite_api_user_id"]
