import pytest
from bs4 import BeautifulSoup

from django.urls import reverse

from lite_content.lite_internal_frontend.flags import SetFlagsForm


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_put_flags,
    mock_case,
    mock_get_organisation,
    mock_flagging_rules,
    mock_countries,
    mock_flag_get,
    mock_flagging_rule_get,
):
    yield


def test_flags_cannot_be_created_and_modified(authorized_client, reset_config_users_list):

    url = reverse("flags:flags")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == False


def test_flags_can_be_created_and_modified(authorized_client, specify_config_users_list):

    url = reverse("flags:flags")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == True


def test_flagging_rules_cannot_be_created_and_modified(authorized_client, reset_config_users_list):

    url = reverse("flags:flagging_rules")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == False


def test_flagging_rules_can_be_created_and_modified(authorized_client, specify_config_users_list):

    url = reverse("flags:flagging_rules")
    response = authorized_client.get(url)
    assert response.status_code == 200
    assert response.context["can_change_config"] == True


@pytest.mark.parametrize(
    "url",
    (
        (reverse("flags:add")),
        (reverse("flags:edit", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
        (reverse("flags:change_status", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234", "status": "Active"})),
    ),
)
def test_flags_add_view_returns_unauthorized_user_not_on_config_admin_list(
    authorized_client, reset_config_users_list, url
):

    response = authorized_client.get(url)
    assert response.status_code == 403
    assert response.context["title"] == "Sorry, unauthorized"
    assert response.context["description"] == "You don't have authorisation to view this page"


@pytest.mark.parametrize(
    "url",
    (
        (reverse("flags:add")),
        (reverse("flags:edit", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
        (reverse("flags:change_status", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234", "status": "deactivate"})),
    ),
)
def test_flags_add_view_returns_ok_user_on_config_admin_list(authorized_client, specify_config_users_list, url):

    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "url",
    (
        (reverse("flags:create_flagging_rules")),
        (reverse("flags:edit_flagging_rule", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
        (
            reverse(
                "flags:change_flagging_rule_status",
                kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234", "status": "Active"},
            )
        ),
    ),
)
def test_flagging_rules_add_view_returns_unauthorized_user_not_on_config_admin_list(
    authorized_client, reset_config_users_list, url
):

    response = authorized_client.get(url)
    assert response.status_code == 403
    assert response.context["title"] == "Sorry, unauthorized"
    assert response.context["description"] == "You don't have authorisation to view this page"


@pytest.mark.parametrize(
    "url",
    (
        (reverse("flags:create_flagging_rules")),
        (reverse("flags:edit_flagging_rule", kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234"})),
        (
            reverse(
                "flags:change_flagging_rule_status",
                kwargs={"pk": "e9f8711e-b383-47e5-b160-153f27771234", "status": "Active"},
            )
        ),
    ),
)
def test_flagging_rules_add_view_returns_ok_user_on_config_admin_list(
    authorized_client, specify_config_users_list, url
):

    response = authorized_client.get(url)
    assert response.status_code == 200


def test_assign_flags_view_destination(authorized_client, queue_pk, open_case_pk):
    url = reverse("cases:assign_flags", kwargs={"queue_pk": queue_pk, "pk": open_case_pk})
    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    form = soup.find("form")

    assert SetFlagsForm.Destinations.TITLE in str(form)


def test_assign_flags_form_goods(authorized_client, data_standard_case, queue_pk, standard_case_pk):

    good_pk = data_standard_case["case"]["data"]["goods"][0]["id"]

    url = reverse("cases:assign_flags", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk}) + f"?goods={good_pk}"
    response = authorized_client.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    form = soup.find("form")

    assert SetFlagsForm.Goods.TITLE in str(form)


def test_assign_flags_form_case(authorized_client, data_standard_case, queue_pk, standard_case_pk):

    url = (
        reverse("cases:assign_flags", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk})
        + f"?case={standard_case_pk}"
    )
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    form = soup.find("form")

    assert SetFlagsForm.Cases.TITLE in str(form)
    assert response.status_code == 200


def test_assign_flags_form_organisation(
    authorized_client, data_standard_case, organisation_pk, queue_pk, standard_case_pk
):

    url = reverse("organisations:assign_flags", kwargs={"pk": organisation_pk}) + f"?organisation={organisation_pk}"
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    form = soup.find("form")

    assert SetFlagsForm.Organisations.TITLE in str(form)
    assert response.status_code == 200


def test_assign_flags_goods_form_submit(
    authorized_client, mock_queue, data_standard_case, mock_put_flags, mock_case, queue_pk, standard_case_pk
):

    good_pk = data_standard_case["case"]["data"]["goods"][0]["good"]["id"]

    valid_data = {
        "note": "Lorem ipsum",
        "flags[]": "",
    }

    url = reverse("cases:assign_flags", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk}) + f"?goods={good_pk}"
    response = authorized_client.get(url)
    assert response.status_code == 200

    response = authorized_client.post(url, data=valid_data)
    assert "#slice-goods" in response.url
    assert response.status_code == 302


def test_assign_flags_destination_form_submit(
    authorized_client, mock_queue, data_standard_case, mock_put_flags, mock_case, queue_pk, standard_case_pk
):

    destination_pk = data_standard_case["case"]["data"]["destinations"]["data"]["id"]

    valid_data = {
        "note": "Lorem ipsum",
        "flags[]": "",
    }

    url = (
        reverse("cases:assign_flags", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk})
        + f"?destinations={destination_pk}"
    )
    response = authorized_client.get(url)
    assert response.status_code == 200

    response = authorized_client.post(url, data=valid_data)
    assert "#slice-destinations" in response.url
    assert response.status_code == 302


def test_assign_flags_case_form_submit(
    authorized_client, mock_queue, data_standard_case, mock_put_flags, mock_case, queue_pk, standard_case_pk
):

    destination_pk = data_standard_case["case"]["data"]["destinations"]["data"]["id"]

    valid_data = {
        "note": "Lorem ipsum",
        "flags[]": "",
    }

    url = (
        reverse("cases:assign_flags", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk})
        + f"?case={standard_case_pk}"
    )
    response = authorized_client.get(url)
    assert response.status_code == 200

    response = authorized_client.post(url, data=valid_data)
    assert response.url == f"/queues/{queue_pk}/cases/{standard_case_pk}/details/"
    assert response.status_code == 302


def test_assign_flags_form_return_to(
    authorized_client, mock_queue, data_standard_case, mock_put_flags, mock_case, queue_pk, standard_case_pk
):

    destination_pk = data_standard_case["case"]["data"]["destinations"]["data"]["id"]

    valid_data = {
        "note": "Lorem ipsum",
        "flags[]": "",
    }

    url = (
        reverse("cases:assign_flags", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk})
        + f"?destinations={destination_pk}&return_to=/foo"
    )
    response = authorized_client.get(url)
    assert response.status_code == 200

    response = authorized_client.post(url, data=valid_data)
    assert response.url == "/foo"
    assert response.status_code == 302
