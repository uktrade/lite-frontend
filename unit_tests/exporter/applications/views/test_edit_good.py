from django.urls import reverse


def test_edit_good_name(authorized_client, data_standard_case, requests_mock):
    application_id = data_standard_case["case"]["data"]["id"]
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = reverse("applications:edit_name", kwargs={"pk": application_id, "good_pk": good["id"]})

    response = authorized_client.post(
        url,
        data={"name": "new good"},
    )

    assert response.status_code == 302
    assert requests_mock.last_request.json() == {"name": "new good"}
