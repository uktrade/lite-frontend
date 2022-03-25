import pytest
import uuid

from pytest_django.asserts import assertContains

from django.urls import reverse

from core import client
from exporter.core.constants import AddGoodFormSteps
from exporter.applications.views.goods.add_good_firearm import AddGoodFirearmSteps
from exporter.goods.forms.firearms import FirearmCategoryForm


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
def control_list_entries(requests_mock):
    requests_mock.get(
        "/static/control-list-entries/", json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]}
    )


def test_firearm_category_redirects_to_new_wizard(
    settings,
    authorized_client,
    requests_mock,
    data_standard_case,
    new_good_firearm_url,
    new_good_url,
):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=app_url, json=data_standard_case["case"])

    clc_url = client._build_absolute_uri("/static/control-list-entries/")
    requests_mock.get(url=clc_url, json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]})

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
    settings, authorized_client, new_good_firearm_url, new_good_url
):
    settings.FEATURE_FLAG_PRODUCT_2_0 = False
    response = authorized_client.get(new_good_firearm_url)
    assert response.status_code == 404


def test_add_good_firearm_start(authorized_client, new_good_firearm_url, new_good_url):
    response = authorized_client.get(new_good_firearm_url)
    assert response.status_code == 200
    assert isinstance(response.context["form"], FirearmCategoryForm)
    assert response.context["hide_step_count"]
    assert response.context["back_link_url"] == new_good_url
    assert response.context["title"] == "Firearm category"


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


def test_add_good_firearm_submission(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
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
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
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
            "category": ["NON_AUTOMATIC_SHOTGUN"],
            "type": "firearms",
        },
        "control_list_entries": ["ML1", "ML1a"],
        "name": "TEST NAME",
        "is_good_controlled": True,
        "is_pv_graded": "no",
        "item_category": "group2_firearms",
    }


def test_add_good_firearm_submission_error(
    authorized_client,
    new_good_firearm_url,
    post_to_step,
    requests_mock,
    data_standard_case,
    control_list_entries,
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
    response = post_to_step(
        AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY,
        {
            "is_good_controlled": True,
            "control_list_entries": [
                "ML1",
                "ML1a",
            ],
        },
    )

    assert response.status_code == 200
    assertContains(response, "Unexpected error adding firearm", html=True)
