from bs4 import BeautifulSoup
import uuid
from django.urls import reverse
from django.conf import settings

from unittest.mock import patch
import pytest

from lite_content.lite_exporter_frontend.goods import CreateGoodForm
from exporter.goods.helpers import get_category_display_string
from exporter.goods.views import GoodSoftwareTechnologyView

from pytest_django.asserts import assertContains

from core.constants import CaseStatusEnum


@pytest.fixture
def good_pk():
    return str(uuid.uuid4())


def test_edit_number_of_items_view(authorized_client, requests_mock, good_pk):
    pk = str(uuid.uuid4())
    url = reverse("applications:number_of_items", kwargs={"pk": pk, "good_pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}", json={"good": {"firearm_details": {"number_of_items": ""}}}
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "number_of_items": "3",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("applications:identification_markings", kwargs={"pk": pk, "good_pk": good_pk})
    assert requests_mock.last_request.json()["number_of_items"] == 3
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Number of items - LITE - GOV.UK"


def test_edit_firearm_product_type_view(authorized_client, requests_mock, good_pk):
    url = reverse("goods:firearm_type", kwargs={"pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}", json={"good": {"firearm_details": {"type": {"key": ""}}}}
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "type": "firearms",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("goods:edit", kwargs={"pk": good_pk})
    assert requests_mock.last_request.json()["type"] == "firearms"
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Select the type of product - LITE - GOV.UK"


def test_edit_identification_markings_view(authorized_client, requests_mock, good_pk):
    url = reverse("goods:identification_markings", kwargs={"pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}",
        json={"good": {"firearm_details": {"serial_numbers_available": "", "no_identification_markings_details": ""}}},
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "serial_numbers_available": "AVAILABLE",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("goods:good", kwargs={"pk": good_pk})
    assert requests_mock.last_request.json()["serial_numbers_available"]
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert (
        soup.title.string.strip()
        == "Will each product have a serial number or other identification marking? - LITE - GOV.UK"
    )


def test_edit_serial_numbers_view(authorized_client, requests_mock, good_pk):
    pk = str(uuid.uuid4())
    url = reverse("applications:serial_numbers", kwargs={"pk": pk, "good_pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}",
        json={"good": {"firearm_details": {"serial_numbers": [], "number_of_items": 2}}},
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "serial_numbers_0": "abcdef",
            "serial_numbers_1": "ghijkl",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("applications:add_good_summary", kwargs={"pk": pk, "good_pk": good_pk})
    data = requests_mock.last_request.json()
    assert data["serial_number_input_0"] == "abcdef"
    assert data["serial_number_input_1"] == "ghijkl"
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Enter the serial numbers for this product - LITE - GOV.UK"


def test_update_serial_numbers_view(authorized_client, requests_mock):
    pk = str(uuid.uuid4())
    good_on_application_pk = str(uuid.uuid4())
    url = reverse(
        "applications:update_serial_numbers", kwargs={"pk": pk, "good_on_application_pk": good_on_application_pk}
    )
    good_name = "Test good"
    serial_numbers = ["11111", "22222"]
    application_url = reverse("applications:application", kwargs={"pk": pk})

    requests_mock.get(
        f"/applications/{pk}/",
        json={
            "id": pk,
            "status": {
                "key": CaseStatusEnum.SUBMITTED,
            },
        },
    )

    requests_mock.get(
        f"/applications/good-on-application/{good_on_application_pk}/",
        json={
            "firearm_details": {
                "number_of_items": len(serial_numbers),
                "serial_numbers": serial_numbers,
            },
            "good": {
                "name": good_name,
            },
            "id": good_on_application_pk,
        },
    )

    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Enter the serial numbers for 'Test good' - LITE - GOV.UK"
    ctx = response.context
    form = ctx["form"]
    assert form.initial == {"serial_numbers": serial_numbers}
    assert form.title == f"Enter the serial numbers for '{good_name}'"
    assert ctx["back_link_url"] == application_url

    update_serial_numbers = ["abcdef", "ghijkl"]

    mock_put = requests_mock.put(
        f"/applications/{pk}/good-on-application/{good_on_application_pk}/update-serial-numbers/",
        json={
            "serial_numbers": update_serial_numbers,
        },
    )

    response = authorized_client.post(
        url,
        data={
            "serial_numbers_0": update_serial_numbers[0],
            "serial_numbers_1": update_serial_numbers[1],
        },
    )
    assert response.status_code == 302
    assert response.url == application_url
    assert mock_put.called_once
    assert mock_put.last_request.json() == {"serial_numbers": ["abcdef", "ghijkl"]}


def test_update_serial_numbers_view_error_exceed_limit(authorized_client, requests_mock):
    pk = str(uuid.uuid4())
    good_on_application_pk = str(uuid.uuid4())
    url = reverse(
        "applications:update_serial_numbers", kwargs={"pk": pk, "good_on_application_pk": good_on_application_pk}
    )
    good_name = "Test good"

    serial_numbers = [str(s) for s in list(range(0, settings.DATA_UPLOAD_MAX_NUMBER_FIELDS + 1))]

    requests_mock.get(
        f"/applications/{pk}/",
        json={
            "id": pk,
            "status": {
                "key": CaseStatusEnum.SUBMITTED,
            },
        },
    )

    requests_mock.get(
        f"/applications/good-on-application/{good_on_application_pk}/",
        json={
            "firearm_details": {
                "number_of_items": len(serial_numbers),
                "serial_numbers": serial_numbers,
            },
            "good": {
                "name": good_name,
            },
            "id": good_on_application_pk,
        },
    )

    update_serial_numbers_dict = {}
    for i, sn in enumerate(serial_numbers):
        update_serial_numbers_dict[f"serial_numbers_{i}"] = sn

    response = authorized_client.post(
        url,
        data=update_serial_numbers_dict,
    )
    assert response.status_code == 400
    assert (
        response.context.flatten()["exception_value"]
        == "The number of GET/POST parameters exceeded settings.DATA_UPLOAD_MAX_NUMBER_FIELDS."
    )


def test_update_serial_numbers_view_error_response(authorized_client, requests_mock, good_pk):
    pk = str(uuid.uuid4())
    good_on_application_pk = str(uuid.uuid4())
    url = reverse(
        "applications:update_serial_numbers", kwargs={"pk": pk, "good_on_application_pk": good_on_application_pk}
    )
    good_name = "Test good"
    serial_numbers = ["11111", "22222"]

    requests_mock.get(
        f"/applications/{pk}/",
        json={
            "id": pk,
            "status": {
                "key": CaseStatusEnum.SUBMITTED,
            },
        },
    )

    requests_mock.get(
        f"/applications/good-on-application/{good_on_application_pk}/",
        json={
            "firearm_details": {
                "number_of_items": len(serial_numbers),
                "serial_numbers": serial_numbers,
            },
            "good": {
                "name": good_name,
            },
            "id": good_on_application_pk,
        },
    )

    update_serial_numbers = ["abcdef", "ghijkl"]

    requests_mock.put(
        f"/applications/{pk}/good-on-application/{good_on_application_pk}/update-serial-numbers/",
        json={
            "errors": {"serial_numbers": "Invalid serial numbers"},
        },
        status_code=400,
    )

    response = authorized_client.post(
        url,
        data={
            "serial_numbers_0": update_serial_numbers[0],
            "serial_numbers_1": update_serial_numbers[1],
        },
    )
    assert response.status_code == 200
    assertContains(response, "Unexpected error updating serial numbers")


def get_update_serial_number_permissions_parameters():
    allowed_application_permissions = [
        CaseStatusEnum.SUBMITTED,
        CaseStatusEnum.FINALISED,
    ]
    all_permissions = CaseStatusEnum.all()
    denied_application_permissions = list(set(all_permissions) - set(allowed_application_permissions))

    parameters = []

    for perm in allowed_application_permissions:
        parameters += [
            (perm, 200),
        ]

    for perm in denied_application_permissions:
        parameters += [
            (perm, 400),
        ]

    return parameters


@pytest.mark.parametrize(
    "application_status, expected_status_code",
    get_update_serial_number_permissions_parameters(),
)
def test_update_serial_numbers_view_permissions(
    authorized_client, requests_mock, good_pk, application_status, expected_status_code
):
    pk = str(uuid.uuid4())
    good_on_application_pk = str(uuid.uuid4())
    url = reverse(
        "applications:update_serial_numbers", kwargs={"pk": pk, "good_on_application_pk": good_on_application_pk}
    )
    good_name = "Test good"
    serial_numbers = ["11111", "22222"]

    requests_mock.get(
        f"/applications/{pk}/",
        json={
            "id": pk,
            "status": {
                "key": application_status,
            },
        },
    )

    requests_mock.get(
        f"/applications/good-on-application/{good_on_application_pk}/",
        json={
            "firearm_details": {
                "number_of_items": len(serial_numbers),
                "serial_numbers": serial_numbers,
            },
            "good": {
                "name": good_name,
            },
            "id": good_on_application_pk,
        },
    )

    response = authorized_client.get(url)
    response.status_code == expected_status_code


def test_good_military_use_view(authorized_client, requests_mock, good_pk):
    url = reverse("goods:good_military_use", kwargs={"pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}",
        json={"good": {"is_military_use": "", "modified_military_use_details": ""}},
    )
    requests_mock.get(
        f"/goods/{good_pk}/?pk={good_pk}&full_detail=True",
        json={"good": {"item_category": {"key": "group3_software"}, "uses_information_security": None}},
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "is_military_use": "yes_designed",
            "modified_military_use_details": "test details",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("goods:good_information_security", kwargs={"pk": good_pk})
    data = requests_mock.request_history[-2].json()
    assert data["is_military_use"] == "yes_designed"
    assert data["modified_military_use_details"] == "test details"
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Is the product for military use? - LITE - GOV.UK"


def test_good_information_security_view(authorized_client, requests_mock, good_pk):
    url = reverse("goods:good_information_security", kwargs={"pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}",
        json={"good": {"uses_information_security": "", "information_security_details": ""}},
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "uses_information_security": True,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("goods:good", kwargs={"pk": good_pk})
    assert requests_mock.last_request.json()["uses_information_security"]
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert (
        soup.title.string.strip()
        == "Is the product designed to employ 'information security' features? - LITE - GOV.UK"
    )


def test_edit_year_of_manufacture_view(authorized_client, requests_mock, good_pk):
    url = reverse("goods:year-of-manufacture", kwargs={"pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}",
        json={"good": {"firearm_details": {"year_of_manufacture": ""}}},
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "year_of_manufacture": 2001,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("goods:good", kwargs={"pk": good_pk})
    assert requests_mock.last_request.json()["firearm_details"]["year_of_manufacture"] == "2001"
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "What is the year of manufacture of the firearm? - LITE - GOV.UK"


def test_edit_firearm_replica_view(authorized_client, requests_mock, good_pk):
    url = reverse("goods:replica", kwargs={"pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}",
        json={"good": {"firearm_details": {"is_replica": "", "replica_description": "", "type": {"key": "firearms"}}}},
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "is_replica": False,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("goods:good", kwargs={"pk": good_pk})
    assert requests_mock.last_request.json()["firearm_details"]["is_replica"] == "False"
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Is the product a replica firearm? - LITE - GOV.UK"


def test_edit_calibre_view(authorized_client, requests_mock, good_pk):
    url = reverse("goods:calibre", kwargs={"pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}",
        json={"good": {"firearm_details": {"calibre": ""}}},
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "calibre": "9mm",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("goods:good", kwargs={"pk": good_pk})
    assert requests_mock.last_request.json()["firearm_details"]["calibre"] == "9mm"
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "What is the calibre of the product? - LITE - GOV.UK"


def test_edit_firearm_act_details_view(authorized_client, requests_mock, good_pk):
    pk = str(uuid.uuid4())
    url = reverse("applications:firearms_act", kwargs={"pk": pk, "good_pk": good_pk})
    requests_mock.get(
        f"/applications/{pk}/",
        json={"organisation": {"documents": {}}},
    )
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}",
        json={
            "good": {
                "firearm_details": {"is_covered_by_firearm_act_section_one_two_or_five": "", "firearms_act_section": ""}
            }
        },
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section1",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("applications:firearms_act_certificate", kwargs={"pk": pk, "good_pk": good_pk})
    data = requests_mock.last_request.json()
    assert data["firearm_details"]["is_covered_by_firearm_act_section_one_two_or_five"] == "Yes"
    assert data["firearm_details"]["firearms_act_section"] == "firearms_act_section1"
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert (
        soup.title.string.strip()
        == "Is the product covered by Section 1, 2 or 5 of the Firearms Act 1968? - LITE - GOV.UK"
    )


def test_good_software_technology_view(authorized_client, requests_mock, good_pk):
    url = reverse("goods:good_software_technology", kwargs={"pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}",
        json={
            "good": {
                "software_or_technology_details": "",
                "item_category": "group2_firearms",
                "firearm_details": {"type": {"key": ""}},
            }
        },
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={
            "software_or_technology_details": "test details",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("goods:good", kwargs={"pk": good_pk})
    assert requests_mock.last_request.json()["software_or_technology_details"] == "test details"
    with patch(
        "exporter.goods.views.GoodSoftwareTechnologyView.get_form_title",
        return_value="Describe the purpose of the software",
    ):
        response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Describe the purpose of the software - LITE - GOV.UK"


def test_good_component_view(authorized_client, requests_mock, good_pk):
    url = reverse("goods:good_component", kwargs={"pk": good_pk})
    requests_mock.get(
        f"/goods/{good_pk}/details/?pk={good_pk}",
        json={
            "good": {
                "is_component": "",
                "component_details": "group2_firearms",
            }
        },
    )
    requests_mock.put(f"/goods/{good_pk}/details/", json={})

    response = authorized_client.post(
        url,
        data={"is_component": "yes_designed", "designed_details": "test details"},
    )

    assert response.status_code == 302
    assert response.url == reverse("goods:good", kwargs={"pk": good_pk})
    data = requests_mock.last_request.json()
    assert data["is_component"] == "yes_designed"
    assert data["designed_details"] == "test details"
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Is the product a component? - LITE - GOV.UK"


def test_goods_recipients_form_view(authorized_client, requests_mock):
    pk = str(uuid.uuid4())
    requests_mock.get(f"/applications/{pk}/", json={})
    url = reverse("applications:goods_recipients", kwargs={"pk": pk})
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Who are the products going to? - LITE - GOV.UK"


def test_permanent_or_temporary_export_form_view(authorized_client, requests_mock):
    pk = str(uuid.uuid4())
    requests_mock.get(f"/applications/{pk}/", json={})
    url = reverse("applications:temporary_or_permanent", kwargs={"pk": pk})
    with patch(
        "exporter.applications.views.locations.TemporaryOrPermanentFormView.get_initial", return_value="temporary"
    ):
        response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Are the products being permanently exported? - LITE - GOV.UK"


def test_goods_starting_point_form(authorized_client, requests_mock):
    pk = str(uuid.uuid4())
    requests_mock.get(f"/applications/{pk}/", json={})
    url = reverse("applications:edit_location", kwargs={"pk": pk})
    with patch(
        "exporter.applications.views.locations.GoodsStartingPointFormView.get_initial",
        return_value="Goods Starting Point",
    ):
        response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.title.string.strip() == "Where will the products begin their export journey? - LITE - GOV.UK"


def test_good_software_technology_view_get_form_title():
    view_instance = GoodSoftwareTechnologyView()

    def mock_get_category_type():
        return "group3_software"

    view_instance.get_category_type = mock_get_category_type

    expected_title = CreateGoodForm.TechnologySoftware.TITLE + get_category_display_string("group3_software")
    actual_title = view_instance.get_form_title()

    assert expected_title == actual_title
