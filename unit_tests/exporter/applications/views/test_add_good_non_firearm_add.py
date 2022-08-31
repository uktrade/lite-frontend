import pytest
import uuid

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_COMPONENTS_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_SOFTWARE_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_MATERIAL_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_PLATFORM_ENABLED = True


@pytest.fixture
def application_pk():
    return str(uuid.uuid4())


def test_is_good_firearm_form(authorized_client, application_pk):
    url = reverse("applications:is_good_firearm", kwargs={"pk": application_pk})
    response = authorized_client.get(url)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "post_url",
    (
        "new_good_firearm",
        "non_firearm_category",
    ),
)
def test_is_good_firearm_view_raise_404(authorized_client, application_pk, post_url, settings):
    settings.FEATURE_FLAG_NON_FIREARMS_ENABLED = False
    url = reverse(f"applications:{post_url}", kwargs={"pk": application_pk})
    response = authorized_client.get(url)
    assert response.status_code == 404


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
        ("PLATFORM", "new_good_platform"),
        ("SOFTWARE", "new_good_software"),
        ("MATERIAL_CATEGORY", "is_material_substance"),
    ),
)
def test_non_firearm_category_select(authorized_client, application_pk, data, redirect_url):
    url = reverse("applications:non_firearm_category", kwargs={"pk": application_pk})
    response = authorized_client.post(url, data={"no_firearm_category": data})
    assert response.status_code == 302
    assert response.url == reverse(f"applications:{redirect_url}", kwargs={"pk": application_pk})


@pytest.mark.parametrize(
    "data, redirect_url",
    (
        (True, "new_good_material"),
        (False, "new_good_component"),
    ),
)
def test_is_material_substance_select(authorized_client, application_pk, data, redirect_url):
    url = reverse("applications:is_material_substance", kwargs={"pk": application_pk})
    response = authorized_client.post(url, data={"is_material_substance": data})
    assert response.status_code == 302
    assert response.url == reverse(f"applications:{redirect_url}", kwargs={"pk": application_pk})


def test_is_material_substance_404(authorized_client, application_pk, settings):
    settings.FEATURE_FLAG_NON_FIREARMS_COMPONENTS_ENABLED = False
    settings.FEATURE_FLAG_NON_FIREARMS_MATERIAL_ENABLED = False
    url = reverse("applications:is_material_substance", kwargs={"pk": application_pk})
    response = authorized_client.post(url, data={"is_material_substance": True})
    assert response.status_code == 404
