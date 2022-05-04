from bs4 import BeautifulSoup
from django.urls import reverse
import pytest

from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:tau:edit",
        kwargs={
            "queue_pk": data_queue["id"],
            "pk": data_standard_case["case"]["id"],
            "good_id": data_standard_case["case"]["data"]["goods"][1]["id"],
        },
    )


def get_cells(soup, table_id):
    return [td.text for td in soup.find(id=table_id).find_all("td")]


def test_tau_edit_auth(authorized_client, url, mock_control_list_entries, mock_precedents_api):
    """GET edit should return 200 with an authorised client"""
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_tau_home_noauth(client, url):
    """GET edit should return 302 with an unauthorised client"""
    response = client.get(url)
    assert response.status_code == 302


def test_form(
    authorized_client, url, data_standard_case, requests_mock, mock_control_list_entries, mock_precedents_api
):
    """
    Tests the submission of a valid form only. More tests on the form itself are in test_forms.py
    """
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]
    requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )
    # Get the edit form
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the form fields contain sane values
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    # Check control list entries
    edit_good_cle = [cle["rating"] for cle in edit_good["control_list_entries"]]
    form_cle = [cle.attrs["value"] for cle in soup.find("form").find_all("option") if "selected" in cle.attrs]
    assert edit_good_cle == form_cle
    # Check report summary
    assert edit_good["report_summary"] == soup.find("form").find(id="report_summary").attrs["value"]
    # Check comments
    assert edit_good["comment"] == soup.find("form").find(id="id_comment").text.strip()

    # Post the form with changes to data
    response = authorized_client.post(
        url, data={"report_summary": "test", "does_not_have_control_list_entries": True, "comment": "test"}
    )

    # Check response and API payload
    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "control_list_entries": [],
        "report_summary": "test",
        "comment": "test",
        "current_object": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "objects": ["6a7fc61f-698b-46b6-9876-6ac0fddfb1a2"],
        "is_good_controlled": False,
        "is_wassenaar": False,
    }
