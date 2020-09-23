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
