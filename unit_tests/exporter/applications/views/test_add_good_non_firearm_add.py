import pytest
import uuid

from django.urls import reverse


@pytest.fixture
def application_pk():
    return str(uuid.uuid4())


def test_is_good_firearm_form(authorized_client, application_pk):
    url = reverse("applications:is_good_firearm", kwargs={"pk": application_pk})
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "data, post_url",
    (
        ({"is_firearm_product": True}, "new_good"),
        ({"is_firearm_product": False}, "non_firearm_category"),
    ),
)
def test_good_non_firearm_post(authorized_client, application_pk, data, post_url):
    url = reverse("applications:is_good_firearm", kwargs={"pk": application_pk})
    response = authorized_client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == reverse(f"applications:{post_url}", kwargs={"pk": application_pk})


def test_non_firearm_category(authorized_client, application_pk):
    url = reverse("applications:non_firearm_category", kwargs={"pk": application_pk})
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "data, redirect_url",
    (
        ("TECHNOLOGY", "new_good_technology"),
        ("COMPLETE_ITEM", "new_good_complete_item"),
        ("MATERIAL_CATEGORY", "is_material_substance"),
    ),
)
def test_non_firearm_category_select(authorized_client, application_pk, data, redirect_url):
    url = reverse("applications:non_firearm_category", kwargs={"pk": application_pk})
    response = authorized_client.post(url, data={"no_firearm_category": data})
    assert response.status_code == 302
    assert response.url == reverse(f"applications:{redirect_url}", kwargs={"pk": application_pk})


@pytest.fixture
def is_material_substance_url(application_pk):
    return reverse("applications:is_material_substance", kwargs={"pk": application_pk})


@pytest.mark.parametrize(
    "data, redirect_url",
    (
        (True, "new_good_material"),
        (False, "new_good_component_accessory"),
    ),
)
def test_is_material_substance_select(authorized_client, application_pk, data, redirect_url, is_material_substance_url):
    response = authorized_client.post(is_material_substance_url, data={"is_material_substance": data})
    assert response.status_code == 302
    assert response.url == reverse(f"applications:{redirect_url}", kwargs={"pk": application_pk})


def test_is_material_substance_context_data(authorized_client, application_pk, is_material_substance_url):
    response = authorized_client.get(is_material_substance_url)
    assert response.status_code == 200
    assert response.context["back_link_url"] == reverse(
        "applications:non_firearm_category", kwargs={"pk": application_pk}
    )
