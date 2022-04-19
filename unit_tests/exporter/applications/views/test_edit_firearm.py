import pytest

from django.core.files.storage import Storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from unittest.mock import patch

from exporter.applications.views.goods.add_good_firearm.views.constants import AddGoodFirearmSteps


@pytest.fixture(autouse=True)
def setup(
    mock_application_get,
    mock_good_get,
    mock_good_put,
    mock_control_list_entries_get,
    mock_good_document_post,
    mock_good_document_put,
    mock_good_document_delete,
    settings,
    no_op_storage,
):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture(autouse=True)
def application(data_standard_case):
    return data_standard_case["case"]["data"]


@pytest.fixture(autouse=True)
def good_on_application(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]["good"]


@pytest.fixture(autouse=True)
def edit_pv_grading_url(application, good_on_application):
    return reverse(
        "applications:firearm_edit_pv_grading",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )


@pytest.fixture
def edit_product_availability_url(application, good_on_application):
    return reverse(
        "applications:firearm_edit_product_document_availability",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )


@pytest.fixture
def edit_product_sensitivity_url(application, good_on_application):
    return reverse(
        "applications:firearm_edit_product_document_sensitivity",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )


@pytest.fixture(autouse=True)
def product_document():
    return {
        "product_document": SimpleUploadedFile("data sheet", b"This is a detailed spec of this Rifle"),
        "description": "product data sheet",
    }


@pytest.mark.parametrize(
    "url_name, form_data, expected",
    (
        (
            "firearm_edit_name",
            {"name": "new good"},
            {"name": "new good"},
        ),
        (
            "firearm_edit_category",
            {"category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_HANDGUN"]},
            {"firearm_details": {"category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_HANDGUN"]}},
        ),
        ("firearm_edit_calibre", {"calibre": "2"}, {"firearm_details": {"calibre": "2"}}),
        (
            "firearm_edit_replica",
            {"is_replica": True, "replica_description": "photocopy of real item"},
            {"firearm_details": {"is_replica": True, "replica_description": "photocopy of real item"}},
        ),
        (
            "firearm_edit_replica",
            {"is_replica": False, "replica_description": "photocopy of real item"},
            {"firearm_details": {"is_replica": False, "replica_description": ""}},
        ),
    ),
)
def test_edit_firearm(
    authorized_client, requests_mock, application, good_on_application, url_name, form_data, expected
):
    url = reverse(f"applications:{url_name}", kwargs={"pk": application["id"], "good_pk": good_on_application["id"]})

    response = authorized_client.post(
        url,
        data=form_data,
    )

    assert response.status_code == 302
    assert requests_mock.last_request.json() == expected


@pytest.mark.parametrize(
    "data, expected",
    (
        (
            {"is_good_controlled": False},
            {"is_good_controlled": False, "control_list_entries": []},
        ),
        (
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
            {"is_good_controlled": True, "control_list_entries": ["ML1a", "ML22b"]},
        ),
    ),
)
def test_edit_good_control_list_entry_options(
    authorized_client, requests_mock, application, good_on_application, data, expected
):
    url = reverse(
        "applications:firearm_edit_control_list_entries",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )

    response = authorized_client.post(url, data=data)

    assert response.status_code == 302
    assert requests_mock.last_request.json() == expected


@pytest.fixture
def goto_step_pv_grading(goto_step_factory, edit_pv_grading_url):
    return goto_step_factory(edit_pv_grading_url)


@pytest.fixture
def post_to_step_pv_grading(post_to_step_factory, edit_pv_grading_url):
    return post_to_step_factory(edit_pv_grading_url)


def test_edit_pv_grading(
    requests_mock, pv_gradings, goto_step_pv_grading, post_to_step_pv_grading, edit_pv_grading_url
):
    response = goto_step_pv_grading(AddGoodFirearmSteps.PV_GRADING)
    assert response.status_code == 200

    response = post_to_step_pv_grading(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": True},
    )

    assert response.status_code == 200

    response = post_to_step_pv_grading(
        AddGoodFirearmSteps.PV_GRADING_DETAILS,
        {
            "prefix": "NATO",
            "grading": "official",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue_0": "20",
            "date_of_issue_1": "02",
            "date_of_issue_2": "2020",
        },
    )

    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "is_pv_graded": "yes",
        "pv_grading_details": {
            "prefix": "NATO",
            "grading": "official",
            "suffix": "",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue": "2020-02-20",
        },
    }


def test_edit_pv_grading_details(authorized_client, application, good_on_application, requests_mock, pv_gradings):
    url = reverse(
        "applications:firearm_edit_pv_grading_details",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )

    response = authorized_client.post(
        url,
        data={
            "prefix": "NATO",
            "grading": "official",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue_0": "20",
            "date_of_issue_1": "02",
            "date_of_issue_2": "2020",
        },
    )

    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "is_pv_graded": "yes",
        "pv_grading_details": {
            "prefix": "NATO",
            "grading": "official",
            "suffix": "",
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue": "2020-02-20",
        },
    }


def test_edit_product_document_upload_form(
    authorized_client, requests_mock, application, good_on_application, product_document, product_summary_url
):
    url = reverse(
        "applications:firearm_edit_product_document",
        kwargs={"pk": application["id"], "good_pk": good_on_application["id"]},
    )
    response = authorized_client.post(url, data=product_document)

    assert response.status_code == 302
    assert response.url == product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.last_request.json() == [
        {"name": "data sheet", "s3_key": "data sheet", "size": 0, "description": "product data sheet"}
    ]


def test_edit_product_document_is_sensitive(
    requests_mock, post_to_step_edit_product_document_sensitivity, product_summary_url
):
    response = post_to_step_edit_product_document_sensitivity(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": True},
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    # if any document exists then we delete that one
    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.last_request.json() == {"is_document_sensitive": True}


@pytest.fixture
def post_to_step_edit_product_document_sensitivity(post_to_step_factory, edit_product_sensitivity_url):
    return post_to_step_factory(edit_product_sensitivity_url)


def test_upload_new_product_document_to_replace_existing_one(
    requests_mock,
    post_to_step_edit_product_document_sensitivity,
    product_document,
    product_summary_url,
):
    response = post_to_step_edit_product_document_sensitivity(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": False},
    )
    response = post_to_step_edit_product_document_sensitivity(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD,
        data=product_document,
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == [
        {"name": "data sheet", "s3_key": "data sheet", "size": 0, "description": "product data sheet"}
    ]

    assert requests_mock.request_history.pop().json() == {"is_document_sensitive": False}


@pytest.fixture
def post_to_step_edit_product_document_availability(post_to_step_factory, edit_product_availability_url):
    return post_to_step_factory(edit_product_availability_url)


def test_edit_product_document_availability_select_not_available(
    requests_mock, post_to_step_edit_product_document_availability, product_summary_url
):
    response = post_to_step_edit_product_document_availability(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        data={"is_document_available": False, "no_document_comments": "Product not manufactured yet"},
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == {
        "is_document_available": False,
        "no_document_comments": "Product not manufactured yet",
    }


def test_edit_product_document_availability_select_available_but_sensitive(
    requests_mock, post_to_step_edit_product_document_availability, product_summary_url
):
    response = post_to_step_edit_product_document_availability(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        data={"is_document_available": True},
    )
    response = post_to_step_edit_product_document_availability(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": True},
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == {
        "is_document_available": True,
        "no_document_comments": "",
        "is_document_sensitive": True,
    }


def test_edit_product_document_availability_upload_new_document(
    requests_mock, post_to_step_edit_product_document_availability, product_document, product_summary_url
):
    response = post_to_step_edit_product_document_availability(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY,
        data={"is_document_available": True},
    )
    response = post_to_step_edit_product_document_availability(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY,
        data={"is_document_sensitive": False},
    )
    response = post_to_step_edit_product_document_availability(
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD,
        data=product_document,
    )

    assert response.status_code == 302
    assert response.url == product_summary_url

    document_delete_request = requests_mock.request_history.pop()
    assert document_delete_request.method == "DELETE"
    assert document_delete_request.matcher.called_once

    assert requests_mock.request_history.pop().json() == [
        {"name": "data sheet", "s3_key": "data sheet", "size": 0, "description": "product data sheet"}
    ]

    assert requests_mock.request_history.pop().json() == {
        "is_document_available": True,
        "no_document_comments": "",
        "is_document_sensitive": False,
    }
