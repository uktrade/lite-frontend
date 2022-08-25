import pytest
import uuid

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_COMPONENTS_ENABLED = True
    settings.FEATURE_FLAG_NON_FIREARMS_SOFTWARE_ENABLED = True


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


def test_non_firearm_category_select_platform(authorized_client, application_pk):
    url = reverse("applications:non_firearm_category", kwargs={"pk": application_pk})
    response = authorized_client.post(url, data={"no_firearm_category": "PLATFORM"})
    assert response.status_code == 302
    assert response.url == reverse("applications:new_good_platform", kwargs={"pk": application_pk})


def test_non_firearm_category_select_software(authorized_client, application_pk):
    url = reverse("applications:non_firearm_category", kwargs={"pk": application_pk})
    response = authorized_client.post(url, data={"no_firearm_category": "SOFTWARE"})
    assert response.status_code == 302
    assert response.url == reverse("applications:new_good_software", kwargs={"pk": application_pk})
