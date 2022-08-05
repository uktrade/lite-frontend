import pytest

from pytest_django.asserts import assertTemplateUsed
from django.urls import reverse


@pytest.fixture(autouse=True)
def default_feature_flags(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_ENABLED = True


@pytest.fixture
def platform_summary_url(data_standard_case, good_id):
    return reverse(
        "applications:platform_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "good_pk": good_id,
        },
    )


@pytest.fixture
def good(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]


def test_firearm_product_summary_response_status_code(
    authorized_client,
    mock_application_get,
    mock_good_get,
    platform_summary_url,
):
    response = authorized_client.get(platform_summary_url)
    assert response.status_code == 200


def test_firearm_product_summary_template_used(
    authorized_client,
    mock_application_get,
    mock_good_get,
    platform_summary_url,
):
    response = authorized_client.get(platform_summary_url)
    assertTemplateUsed(response, "applications/goods/platform/product-summary.html")


@pytest.fixture
def platform_summary(good_id):
    return (
        (
            "name",
            "p1",
            "Give the product a descriptive name",
        ),
        (
            "is-good-controlled",
            "Yes",
            "Do you know the product's control list entry?",
        ),
        (
            "control-list-entries",
            "ML1a, ML22b",
            "Enter the control list entry",
        ),
        (
            "is-pv-graded",
            "Yes",
            "Does the product have a government security grading or classification?",
        ),
        (
            "pv-grading-prefix",
            "NATO",
            "Enter a prefix (optional)",
        ),
        (
            "pv-grading-grading",
            "Official",
            "What is the security grading or classification?",
        ),
        (
            "pv-grading-suffix",
            "SUFFIX",
            "Enter a suffix (optional)",
        ),
        (
            "pv-grading-issuing-authority",
            "Government entity",
            "Name and address of the issuing authority",
        ),
        (
            "pv-grading-details-reference",
            "GR123",
            "Reference",
        ),
        (
            "pv-grading-details-date-of-issue",
            "20 February 2020",
            "Date of issue",
        ),
    )


def test_firearm_product_summary_context(
    authorized_client,
    mock_application_get,
    mock_good_get,
    platform_summary_url,
    data_standard_case,
    good_id,
    platform_summary,
):
    response = authorized_client.get(platform_summary_url)

    def _get_test_url(name):
        if not name:
            return None
        return f'/applications/{data_standard_case["case"]["id"]}/goods/{good_id}/firearm/edit/{name}/'

    url_map = {
        "name": "name",
        "is-good-controlled": "control-list-entries",
        "control-list-entries": "control-list-entries",
        "is-pv-graded": "pv-grading",
        "pv-grading-prefix": "pv-grading",
        "pv-grading-grading": "pv-grading",
        "pv-grading-suffix": "pv-grading",
        "pv-grading-issuing-authority": "pv-grading",
        "pv-grading-details-reference": "pv-grading",
        "pv-grading-details-date-of-issue": "pv-grading",
    }

    summary_with_links = tuple(
        (key, value, label, _get_test_url(url_map.get(key, None))) for key, value, label in platform_summary
    )

    assert response.context["summary"] == summary_with_links
