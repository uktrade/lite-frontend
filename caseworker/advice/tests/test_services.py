import pytest

from caseworker.advice.services import (
    get_advice_to_consolidate,
    LICENSING_UNIT_TEAM,
    FCDO_TEAM,
    NCSC_TEAM,
    DESNZ_CHEMICAL,
    DESNZ_NUCLEAR,
    MOD_DI_TEAM,
    MOD_DSR_TEAM,
    MOD_DSTL_TEAM,
    MOD_CAPPROT_TEAM,
    MOD_ECJU_TEAM,
)


def test_get_advice_to_consolidate_unrecognized_team_raises_exception():
    with pytest.raises(Exception):
        get_advice_to_consolidate([], "some unknown team")


@pytest.mark.parametrize(
    "advice, expected_grouping",
    (
        # No advice to group
        ([], {}),
        # FCDO advice only
        (
            [
                {
                    "id": "advice-1",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
            ],
            {
                "id-fcdo-approve": [
                    {
                        "id": "advice-1",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                    }
                ]
            },
        ),
        # FCDO and MOD-DI advice only
        (
            [
                {
                    "id": "advice-1",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
                {
                    "id": "advice-2",
                    "level": "team",
                    "type": {"key": "approve"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
                {
                    "id": "advice-3",
                    "level": "team",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                },
            ],
            {
                "id-fcdo-approve": [
                    {
                        "id": "advice-1",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                    },
                    {
                        "id": "advice-2",
                        "level": "team",
                        "type": {"key": "approve"},
                        "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                    },
                ],
                "id-mod-di-approve": [
                    {
                        "id": "advice-3",
                        "level": "team",
                        "type": {"key": "approve"},
                        "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                    },
                ],
            },
        ),
        # All OGDs advising with MOD collected under MOD-ECJU
        (
            [
                {
                    "id": "advice-1",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
                {
                    "id": "advice-2",
                    "level": "team",
                    "type": {"key": "approve"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
                {
                    "id": "advice-2",
                    "level": "team",
                    "type": {"key": "proviso"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
                {
                    "id": "advice-3",
                    "level": "team",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                },
                {
                    "id": "advice-4",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                },
                {
                    "id": "advice-4",
                    "level": "user",
                    "type": {"key": "refuse"},
                    "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                },
                {
                    "id": "advice-5",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": DESNZ_NUCLEAR, "id": "id-desnz-nuclear"},
                },
                {
                    "id": "advice-6",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": DESNZ_CHEMICAL, "id": "id-desnz-chemical"},
                },
                {
                    "id": "advice-6",
                    "level": "user",
                    "type": {"key": "refuse"},
                    "team": {"alias": DESNZ_CHEMICAL, "id": "id-desnz-chemical"},
                },
                {
                    "id": "advice-7",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": NCSC_TEAM, "id": "id-ncsc"},
                },
                {
                    "id": "advice-8",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_CAPPROT_TEAM, "id": "id-mod-capprot"},
                },
                {
                    "id": "advice-9",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_DSR_TEAM, "id": "id-mod-dsr"},
                },
                {
                    "id": "advice-10",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_DSTL_TEAM, "id": "id-mod-dstl"},
                },
                {
                    "id": "advice-11",
                    "level": "team",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_ECJU_TEAM, "id": "id-mod-ecju"},
                },
            ],
            {
                "id-fcdo-approve": [
                    {
                        "id": "advice-1",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                    },
                    {
                        "id": "advice-2",
                        "level": "team",
                        "type": {"key": "approve"},
                        "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                    },
                ],
                "id-fcdo-proviso": [
                    {
                        "id": "advice-2",
                        "level": "team",
                        "type": {"key": "proviso"},
                        "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                    },
                ],
                "id-desnz-nuclear-approve": [
                    {
                        "id": "advice-5",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": DESNZ_NUCLEAR, "id": "id-desnz-nuclear"},
                    },
                ],
                "id-desnz-chemical-approve": [
                    {
                        "id": "advice-6",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": DESNZ_CHEMICAL, "id": "id-desnz-chemical"},
                    },
                ],
                "id-desnz-chemical-refuse": [
                    {
                        "id": "advice-6",
                        "level": "user",
                        "type": {"key": "refuse"},
                        "team": {"alias": DESNZ_CHEMICAL, "id": "id-desnz-chemical"},
                    },
                ],
                "id-ncsc-approve": [
                    {
                        "id": "advice-7",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": NCSC_TEAM, "id": "id-ncsc"},
                    },
                ],
                "id-mod-ecju-approve": [
                    {
                        "id": "advice-11",
                        "level": "team",
                        "type": {"key": "approve"},
                        "team": {"alias": MOD_ECJU_TEAM, "id": "id-mod-ecju"},
                    },
                ],
                "id-mod-di-approve": [
                    {
                        "id": "advice-3",
                        "level": "team",
                        "type": {"key": "approve"},
                        "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                    },
                    {
                        "id": "advice-4",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                    },
                ],
                "id-mod-di-refuse": [
                    {
                        "id": "advice-4",
                        "level": "user",
                        "type": {"key": "refuse"},
                        "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                    },
                ],
            },
        ),
    ),
)
def test_get_advice_to_consolidate_lu(advice, expected_grouping):
    assert get_advice_to_consolidate(advice, LICENSING_UNIT_TEAM) == expected_grouping


@pytest.mark.parametrize(
    "advice, expected_grouping",
    (
        # No advice to group
        ([], {}),
        # FCDO advice only
        (
            [
                {
                    "id": "advice-1",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
            ],
            {},
        ),
        # FCDO and MOD-DI advice only
        (
            [
                {
                    "id": "advice-1",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
                {
                    "id": "advice-2",
                    "level": "team",
                    "type": {"key": "approve"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
                {
                    "id": "advice-3",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                },
                {
                    "id": "advice-3",
                    "level": "user",
                    "type": {"key": "refuse"},
                    "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                },
            ],
            {
                "id-mod-di-approve": [
                    {
                        "id": "advice-3",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                    },
                ],
                "id-mod-di-refuse": [
                    {
                        "id": "advice-3",
                        "level": "user",
                        "type": {"key": "refuse"},
                        "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                    },
                ],
            },
        ),
        # All OGDs advising with MOD collected under MOD-ECJU
        (
            [
                {
                    "id": "advice-1",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
                {
                    "id": "advice-2",
                    "level": "team",
                    "type": {"key": "approve"},
                    "team": {"alias": FCDO_TEAM, "id": "id-fcdo"},
                },
                {
                    "id": "advice-3",
                    "level": "team",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                },
                {
                    "id": "advice-4",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                },
                {
                    "id": "advice-5",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": DESNZ_NUCLEAR, "id": "id-desnz-nuclear"},
                },
                {
                    "id": "advice-6",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": DESNZ_CHEMICAL, "id": "id-desnz-chemical"},
                },
                {
                    "id": "advice-7",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": NCSC_TEAM, "id": "id-ncsc"},
                },
                {
                    "id": "advice-8",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_CAPPROT_TEAM, "id": "id-mod-capprot"},
                },
                {
                    "id": "advice-9",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_DSR_TEAM, "id": "id-mod-dsr"},
                },
                {
                    "id": "advice-10",
                    "level": "user",
                    "type": {"key": "approve"},
                    "team": {"alias": MOD_DSTL_TEAM, "id": "id-mod-dstl"},
                },
            ],
            {
                "id-mod-di-approve": [
                    {
                        "id": "advice-4",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"},
                    },
                ],
                "id-mod-capprot-approve": [
                    {
                        "id": "advice-8",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": MOD_CAPPROT_TEAM, "id": "id-mod-capprot"},
                    },
                ],
                "id-mod-dsr-approve": [
                    {
                        "id": "advice-9",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": MOD_DSR_TEAM, "id": "id-mod-dsr"},
                    },
                ],
                "id-mod-dstl-approve": [
                    {
                        "id": "advice-10",
                        "level": "user",
                        "type": {"key": "approve"},
                        "team": {"alias": MOD_DSTL_TEAM, "id": "id-mod-dstl"},
                    },
                ],
            },
        ),
    ),
)
def test_get_advice_to_consolidate_mod_ecju(advice, expected_grouping):
    assert get_advice_to_consolidate(advice, MOD_ECJU_TEAM) == expected_grouping
