import pytest

from caseworker.flags.services import _add_flag_permissions


@pytest.mark.parametrize(
    "permissions, num_unremovable",
    [
        ([], 3),
        (["REMOVE_AUTHORISED_COUNTERSIGNER_FLAGS"], 2),
        (["REMOVE_HEAD_OF_LICENSING_UNIT_FLAGS"], 1),
        (
            [
                "REMOVE_AUTHORISED_COUNTERSIGNER_FLAGS",
                "REMOVE_HEAD_OF_LICENSING_UNIT_FLAGS",
            ],
            0,
        ),
    ],
)
def test_get_flags_permissions(permissions, num_unremovable):
    data = [
        {
            "id": "00000000-0000-0000-0000-000000000014",
            "name": "Flag 2",
            "colour": "default",
            "level": "Case",
            "label": None,
            "status": "Active",
            "priority": 0,
            "blocks_finalising": False,
            "removable_by": "Anyone",
            "team": {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin"},
        },
        {
            "id": "00000000-0000-0000-0000-000000000015",
            "name": "Flag 1",
            "colour": "default",
            "level": "Case",
            "label": None,
            "status": "Active",
            "priority": 0,
            "blocks_finalising": True,
            "removable_by": "Anyone",
            "team": {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin"},
        },
        {
            "id": "00000000-0000-0000-0000-000000000016",
            "name": "Flag 3",
            "colour": "default",
            "level": "Case",
            "label": None,
            "status": "Active",
            "priority": 0,
            "blocks_finalising": True,
            "removable_by": "Authorised countersigner",
            "team": {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin"},
        },
        {
            "id": "00000000-0000-0000-0000-000000000017",
            "name": "Flag 3",
            "colour": "default",
            "level": "Case",
            "label": None,
            "status": "Active",
            "priority": 0,
            "blocks_finalising": True,
            "removable_by": "Head of Licensing Unit countersigner",
            "team": {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin"},
        },
        {
            "id": "00000000-0000-0000-0000-000000000018",
            "name": "Flag 4",
            "colour": "default",
            "level": "Case",
            "label": None,
            "status": "Active",
            "priority": 0,
            "blocks_finalising": True,
            "removable_by": "Head of Licensing Unit countersigner",
            "team": {"id": "00000000-0000-0000-0000-000000000001", "name": "Admin"},
        },
    ]
    flags = _add_flag_permissions(data, permissions)
    unremovable_flags = [flag for flag in flags if flag["cannot_remove"]]
    assert len(unremovable_flags) == num_unremovable
