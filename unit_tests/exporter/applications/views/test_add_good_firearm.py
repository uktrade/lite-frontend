import pytest
import uuid

from pytest_django.asserts import assertContains

from django.urls import reverse

from core import client
from exporter.core.constants import AddGoodFormSteps
from exporter.applications.views.goods.add_good_firearm import AddGoodFirearmSteps
from exporter.goods.forms.firearms import (
    FirearmCategoryForm,
    FirearmRFDValidityForm,
)


@pytest.fixture
def new_good_url(data_standard_case):
    return reverse("applications:new_good", kwargs={"pk": data_standard_case["case"]["id"]})


@pytest.fixture
def new_good_firearm_url(data_standard_case):
    return reverse(
        "applications:new_good_firearm",
        kwargs={
            "pk": data_standard_case["case"]["id"],
        },
    )


@pytest.fixture(autouse=True)
def set_feature_flags(settings):
    settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS = True
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def application(data_standard_case, requests_mock):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    matcher = requests_mock.get(url=app_url, json=data_standard_case["case"])
    return matcher


@pytest.fixture
def rfd_certificate():
    return {
        "id": str(uuid.uuid4()),
        "document": {
            "name": "testdocument.txt",
        },
        "document_type": "rfd-certificate",
        "is_expired": False,
    }


@pytest.fixture
def application_with_rfd_document(data_standard_case, requests_mock, rfd_certificate):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    case = data_standard_case["case"]
    case["organisation"] = {
        "documents": [rfd_certificate],
    }
    matcher = requests_mock.get(url=app_url, json=case)
    return matcher


@pytest.fixture
def application_without_rfd_document(application):
    return application


@pytest.fixture
def control_list_entries(requests_mock):
    clc_url = client._build_absolute_uri("/static/control-list-entries/")
    matcher = requests_mock.get(url=clc_url, json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]})
    return matcher


@pytest.fixture
def pv_gradings(requests_mock):
    requests_mock.get(
        "/static/private-venture-gradings/v2/",
        json={"pv_gradings": [{"official": "Official"}, {"restricted": "Restricted"}]},
    )


def test_firearm_category_redirects_to_new_wizard(
    authorized_client,
    new_good_firearm_url,
    new_good_url,
    application,
    control_list_entries,
):
    response = authorized_client.post(new_good_url, data={"wizard_goto_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE})
    response = authorized_client.post(
        new_good_url,
        data={
            f"add_good-current_step": AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE,
            f"{AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE}-type": "firearms",
        },
    )

    assert response.status_code == 302
    assert response.url == new_good_firearm_url


def test_add_good_firearm_access_denied_without_feature_flag(
    settings,
    authorized_client,
    new_good_firearm_url,
):
    settings.FEATURE_FLAG_PRODUCT_2_0 = False
    response = authorized_client.get(new_good_firearm_url)
    assert response.status_code == 404


def test_add_good_firearm_invalid_application(
    data_standard_case, requests_mock, authorized_client, new_good_firearm_url
):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=app_url, status_code=404)
    response = authorized_client.get(new_good_firearm_url)
    assert response.status_code == 404


def test_add_good_firearm_start(authorized_client, new_good_firearm_url, new_good_url, application):
    response = authorized_client.get(new_good_firearm_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmCategoryForm)
    assert response.context["hide_step_count"]
    assert response.context["back_link_url"] == new_good_url
    assert response.context["title"] == "Firearm category"


@pytest.fixture
def goto_step(authorized_client, new_good_firearm_url):
    def _goto_step(step_name):
        return authorized_client.post(
            new_good_firearm_url,
            data={
                "wizard_goto_step": step_name,
            },
        )

    return _goto_step


@pytest.fixture
def post_to_step(authorized_client, new_good_firearm_url):
    ADD_GOOD_FIREARM_VIEW = "add_good_firearm"

    def _post_to_step(step_name, data):
        return authorized_client.post(
            new_good_firearm_url,
            data={
                f"{ADD_GOOD_FIREARM_VIEW}-current_step": step_name,
                **{f"{step_name}-{key}": value for key, value in data.items()},
            },
        )

    return _post_to_step


def test_add_good_firearm_displays_rfd_validity_step(
    application_with_rfd_document, rfd_certificate, goto_step, post_to_step
):
    goto_step(AddGoodFirearmSteps.IS_REPLICA)
    response = post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmRFDValidityForm)
    rfd_certificate_url = reverse("organisation:document", kwargs={"pk": rfd_certificate["id"]})
    assertContains(response, rfd_certificate_url)
    rfd_certificate_name = rfd_certificate["document"]["name"]
    assertContains(response, rfd_certificate_name)


def test_add_good_firearm_submission(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    pv_gradings,
    application_with_rfd_document,
):
    authorized_client.get(new_good_firearm_url)

    good_id = str(uuid.uuid4())

    post_goods_matcher = requests_mock.post(
        f"/goods/",
        status_code=201,
        json={
            "good": {
                "id": good_id,
            },
        },
    )

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": True},
    )
    post_to_step(
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
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    response = post_to_step(
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID,
        {"is_rfd_valid": True},
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "applications:add_good_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )

    assert post_goods_matcher.called_once
    last_request = post_goods_matcher.last_request
    assert last_request.json() == {
        "firearm_details": {
            "calibre": "calibre 123",
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "is_replica": True,
            "replica_description": "This is a replica",
            "type": "firearms",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": True,
        "prefix": "NATO",
        "grading": "official",
        "suffix": "",
        "issuing_authority": "Government entity",
        "reference": "GR123",
        "date_of_issue": "2020-02-20",
        "item_category": "group2_firearms",
    }


def test_add_good_firearm_submission_error(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
    application_with_rfd_document,
):
    authorized_client.get(new_good_firearm_url)

    requests_mock.post(
        f"/goods/",
        status_code=400,
        json={},
    )

    post_to_step(
        AddGoodFirearmSteps.CATEGORY,
        {"category": ["NON_AUTOMATIC_SHOTGUN"]},
    )
    post_to_step(
        AddGoodFirearmSteps.NAME,
        {"name": "TEST NAME"},
    )
    post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )
    post_to_step(
        AddGoodFirearmSteps.PV_GRADING,
        {"is_pv_graded": False},
    )
    post_to_step(
        AddGoodFirearmSteps.CALIBRE,
        {"calibre": "calibre 123"},
    )
    post_to_step(
        AddGoodFirearmSteps.IS_REPLICA,
        {"is_replica": True, "replica_description": "This is a replica"},
    )
    response = post_to_step(
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID,
        {"is_rfd_valid": True},
    )

    assert response.status_code == 200
    assertContains(response, "Unexpected error adding firearm", html=True)
