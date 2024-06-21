import pytest

from django.urls import reverse

from core import client
from core.constants import FirearmsProductType
from exporter.goods.constants import GoodStatus


@pytest.fixture
def firearm_product_details_url(good_id):
    return reverse(
        "goods:firearm_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def firearm_ammunition_product_details_url(good_id):
    return reverse(
        "goods:firearm_ammunition_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def components_for_firearm_product_details_url(good_id):
    return reverse(
        "goods:components_for_firearms_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def components_for_ammunition_product_details_url(good_id):
    return reverse(
        "goods:components_for_firearms_ammunition_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def firearm_accessory_product_details_url(good_id):
    return reverse(
        "goods:firearms_accessory_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def software_related_to_firearm_product_details_url(good_id):
    return reverse(
        "goods:software_related_to_firearms_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def technology_related_to_firearm_product_details_url(good_id):
    return reverse(
        "goods:technology_related_to_firearms_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def complete_item_product_details_url(good_id):
    return reverse(
        "goods:complete_item_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def material_product_details_url(good_id):
    return reverse(
        "goods:material_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def software_product_details_url(good_id):
    return reverse(
        "goods:technology_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def component_accessory_product_details_url(good_id):
    return reverse(
        "goods:component_accessory_detail",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture(
    params=(
        "firearm_detail",
        "firearm_ammunition_detail",
        "components_for_firearms_detail",
        "components_for_firearms_ammunition_detail",
        "firearms_accessory_detail",
        "software_related_to_firearms_detail",
        "technology_related_to_firearms_detail",
        "complete_item_detail",
        "material_detail",
        "technology_detail",
        "component_accessory_detail",
    )
)
def product_summary_url(request, good_id):
    return request.param, reverse(
        f"goods:{request.param}",
        kwargs={
            "pk": good_id,
        },
    )


@pytest.fixture
def mock_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "status": {"key": GoodStatus.VERIFIED, "value": GoodStatus.VERIFIED.title()},
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
            "section_certificate_missing": True,
            "section_certificate_missing_reason": "No section 5 certificate",
        }
    )
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_firearm_ammunition_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": FirearmsProductType.AMMUNITION, "value": "Ammunition"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
            "section_certificate_missing": True,
            "section_certificate_missing_reason": "No section 5 certificate",
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_components_for_firearm_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": FirearmsProductType.COMPONENTS_FOR_FIREARMS, "value": "Components for firearms"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
            "section_certificate_missing": True,
            "section_certificate_missing_reason": "No section 5 certificate",
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_components_for_ammunition_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": FirearmsProductType.COMPONENTS_FOR_AMMUNITION, "value": "Components for ammunition"},
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "firearms_act_section": "firearms_act_section5",
            "section_certificate_missing": True,
            "section_certificate_missing_reason": "No section 5 certificate",
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_firearm_accessory_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": FirearmsProductType.FIREARMS_ACCESSORY, "value": "Accessory of a firearm"},
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_software_related_to_firearm_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {"key": FirearmsProductType.SOFTWARE_RELATED_TO_FIREARM, "value": "Software relating to a firearm"},
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)


@pytest.fixture
def mock_technology_related_to_firearm_good_get(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["good"].update(
        {
            "is_pv_graded": {"key": "yes", "value": "Yes"},
        }
    )
    good["good"]["firearm_details"].update(
        {
            "type": {
                "key": FirearmsProductType.TECHNOLOGY_RELATED_TO_FIREARM,
                "value": "Technology relating to a firearm",
            },
        }
    )
    del good["good"]["firearm_details"]["category"]
    url = client._build_absolute_uri(f'/goods/{good["good"]["id"]}/')
    return requests_mock.get(url=url, json=good)
