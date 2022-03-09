import pytest
import uuid

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from exporter.applications.views import goods


def test_is_firearm_certificate_needed_has_section_five_certificate():
    actual = goods.is_firearm_certificate_needed(
        application={
            "organisation": {"documents": [{"document_type": "section-five-certificate", "is_expired": False}]}
        },
        selected_section="firearms_act_section5",
    )

    assert actual is False


def test_is_firearm_certificate_needed_no_section_five_certificate():
    actual = goods.is_firearm_certificate_needed(
        application={"organisation": {"documents": []}}, selected_section="firearms_act_section5"
    )

    assert actual is True


def test_is_firearm_certificate_needed_not_section_five_selected():
    actual = goods.is_firearm_certificate_needed(
        application={
            "organisation": {"documents": [{"document_type": "section-five-certificate", "is_expired": False}]}
        },
        selected_section="firearms_act_section2",
    )

    assert actual is True


@pytest.mark.parametrize(
    "expiry_date,error",
    (
        ("2020-01-01", ["Expiry date must be in the future"]),  # Past
        ("2050-01-01", ["Expiry date is too far in the future"]),  # Too far in the future
    ),
)
def test_upload_firearm_registered_dealer_certificate_error(authorized_client, expiry_date, error):
    # How do I write this?
    pass


@pytest.mark.parametrize(
    "expiry_date,error",
    (
        ("2020-01-01", ["Expiry date must be in the future"]),  # Past
        ("2050-01-01", ["Expiry date is too far in the future"]),  # Too far in the future
    ),
)
def test_upload_firearm_section_five_certificate_error(authorized_client, expiry_date, error):
    # How do I write this?
    pass


def test_add_serial_numbers_list(authorized_client, requests_mock):
    applications = [
        {"id": str(uuid.uuid4()), "name": "Application 1"},
        {"id": str(uuid.uuid4()), "name": "Application 2"},
    ]

    requests_mock.get(
        "/applications/require-serial-numbers/?page=1",
        json={
            "results": applications,
        },
    )

    response = authorized_client.get(reverse("applications:add_serial_numbers"))

    assert response.status_code == 200
    assertTemplateUsed(response, "applications/goods/add-serial-numbers-list.html")

    ctx = response.context
    assert ctx["applications"] == applications
