from django.urls import reverse


def test_case_audit_trail_system_user(
    authorized_client, mock_gov_user, mock_case, mock_queue, mock_case_activity_system_user
):
    client = authorized_client(mock_gov_user["user"])
    # given the case has activity from system user
    url = reverse("cases:case", kwargs={"queue_pk": mock_queue["id"], "pk": mock_case["case"]["id"]})

    # when the case is viewed
    response = client.get(url)

    # then it does not error
    assert response.status_code == 200
