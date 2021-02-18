import pytest

from core.builtins import custom_tags
from exporter.core import constants
from exporter.core.objects import Application


@pytest.mark.parametrize(
    "application,expected",
    [
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.STANDARD}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": True,
                    "is_informed_wmd": True,
                    "is_suspected_wmd": True,
                    "is_eu_military": True,
                }
            ),
            constants.DONE,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.STANDARD}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": False,
                    "is_informed_wmd": False,
                    "is_suspected_wmd": False,
                    "is_eu_military": False,
                }
            ),
            constants.DONE,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.STANDARD}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": True,
                    "is_informed_wmd": True,
                    "is_suspected_wmd": True,
                    # missing "is_eu_military"
                }
            ),
            constants.IN_PROGRESS,
        ),
        (Application({"case_type": {"sub_type": {"key": constants.STANDARD}},}), constants.NOT_STARTED),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.OPEN}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": True,
                    "is_informed_wmd": True,
                    "is_suspected_wmd": True,
                }
            ),
            constants.DONE,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.OPEN}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": False,
                    "is_informed_wmd": False,
                    "is_suspected_wmd": False,
                }
            ),
            constants.DONE,
        ),
        (
            Application(
                {
                    "case_type": {"sub_type": {"key": constants.OPEN}},
                    "intended_end_use": "foo",
                    "is_military_end_use_controls": True,
                    "is_informed_wmd": True,
                    # missing "is_suspected_wmd"
                }
            ),
            constants.IN_PROGRESS,
        ),
        (Application({"case_type": {"sub_type": {"key": constants.OPEN}},}), constants.NOT_STARTED),
    ],
)
def test_get_end_use_details_status(application, expected):
    assert custom_tags.get_end_use_details_status(application) == expected


@pytest.mark.parametrize(
    "good_on_app,quantity_display",
    [
        ({"firearm_details": {"type": {"key": "firearms"}}, "quantity": None}, "0 items"),
        ({"firearm_details": {"type": {"key": "firearms"}}, "quantity": 0}, "0 items"),
        ({"firearm_details": {"type": {"key": "firearms"}}, "quantity": 1}, "1 item"),
        ({"firearm_details": {"type": {"key": "firearms"}}, "quantity": 5}, "5 items"),
        ({"firearm_details": {"type": {"key": "ammunition"}}, "quantity": 1}, "1 item"),
        ({"firearm_details": {"type": {"key": "components_for_firearms"}}, "quantity": 5}, "5 items"),
        (
            {
                "firearm_details": {"type": {"key": "software_related_to_firearms"}},
                "quantity": 1,
                "unit": {"key": "NAR", "value": "Number of articles"},
            },
            "1 item",
        ),
        (
            {
                "firearm_details": {"type": {"key": "software_related_to_firearms"}},
                "quantity": 9,
                "unit": {"key": "NAR", "value": "Number of articles"},
            },
            "9 items",
        ),
        (
            {
                "firearm_details": {"type": {"key": "firearms_accessory"}},
                "quantity": 9.0,
                "unit": {"key": "KGM", "value": "Kilogram(s)"},
            },
            "9.0 Kilogram(s)",
        ),
        (
            {
                "firearm_details": {"type": {"key": "firearms_accessory"}},
                "quantity": 9,
                "unit": {"key": "ITG", "value": "Intangible"},
            },
            "9 Intangible",
        ),
    ],
)
def test_pluralise_quantity(good_on_app, quantity_display):
    good_on_app["good"] = {"item_category": {"key": "group2_firearms"}}
    actual = custom_tags.pluralise_quantity(good_on_app)
    assert actual == quantity_display
