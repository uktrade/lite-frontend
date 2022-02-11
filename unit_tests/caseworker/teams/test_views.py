import pytest
from django.urls import reverse

pk = "67b9a4a3-6f3d-4511-8a19-23ccff221a74"


def test_edit_team_view(authorized_client, form_team_data, requests_mock):
    mock_data = {
        "team": {
            "id": "67b9a4a3-6f3d-4511-8a19-23ccff221a74",
            "name": "FCDO",
            "part_of_ecju": True,
            "is_ogd": True,
            "alias": "FCO",
            "department": "3b637abd-283c-4e80-b87e-30c23b0edbec",
        }
    }
    url = reverse("teams:edit", kwargs={"pk": pk})

    requests_mock.get(f"/teams/{pk}/", status_code=200, json=mock_data)
    requests_mock.put(f"/teams/{pk}/", json=form_team_data)

    response = authorized_client.post(url, data=form_team_data)
    assert response.status_code == 302
    history = requests_mock.request_history.pop()
    assert history.method == "PUT"
    assert history.json() == {"is_ogd": True, "name": "Test", "part_of_ecju": True}
