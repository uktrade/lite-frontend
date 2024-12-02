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
                {"id": "advice-1", "level": "user", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
            ],
            {"id-fcdo": [{"id": "advice-1", "level": "user", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}}]},
        ),
        # FCDO and MOD-DI advice only
        (
            [
                {"id": "advice-1", "level": "user", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                {"id": "advice-2", "level": "team", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                {"id": "advice-3", "level": "team", "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"}},
            ],
            {
                "id-fcdo": [
                    {"id": "advice-1", "level": "user", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                    {"id": "advice-2", "level": "team", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                ],
                "id-mod-di": [
                    {"id": "advice-3", "level": "team", "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"}},
                ],
            },
        ),
        # All OGDs advising with MOD collected under MOD-ECJU
        (
            [
                {"id": "advice-1", "level": "user", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                {"id": "advice-2", "level": "team", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                {"id": "advice-3", "level": "team", "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"}},
                {"id": "advice-4", "level": "user", "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"}},
                {"id": "advice-5", "level": "user", "team": {"alias": DESNZ_NUCLEAR, "id": "id-desnz-nuclear"}},
                {"id": "advice-6", "level": "user", "team": {"alias": DESNZ_CHEMICAL, "id": "id-desnz-chemical"}},
                {"id": "advice-7", "level": "user", "team": {"alias": NCSC_TEAM, "id": "id-ncsc"}},
                {"id": "advice-8", "level": "user", "team": {"alias": MOD_CAPPROT_TEAM, "id": "id-mod-capprot"}},
                {"id": "advice-9", "level": "user", "team": {"alias": MOD_DSR_TEAM, "id": "id-mod-dsr"}},
                {"id": "advice-10", "level": "user", "team": {"alias": MOD_DSTL_TEAM, "id": "id-mod-dstl"}},
                {"id": "advice-11", "level": "team", "team": {"alias": MOD_ECJU_TEAM, "id": "id-mod-ecju"}},
            ],
            {
                "id-fcdo": [
                    {"id": "advice-1", "level": "user", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                    {"id": "advice-2", "level": "team", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                ],
                "id-desnz-nuclear": [
                    {"id": "advice-5", "level": "user", "team": {"alias": DESNZ_NUCLEAR, "id": "id-desnz-nuclear"}},
                ],
                "id-desnz-chemical": [
                    {"id": "advice-6", "level": "user", "team": {"alias": DESNZ_CHEMICAL, "id": "id-desnz-chemical"}},
                ],
                "id-ncsc": [
                    {"id": "advice-7", "level": "user", "team": {"alias": NCSC_TEAM, "id": "id-ncsc"}},
                ],
                "id-mod-ecju": [
                    {"id": "advice-11", "level": "team", "team": {"alias": MOD_ECJU_TEAM, "id": "id-mod-ecju"}},
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
                {"id": "advice-1", "level": "user", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
            ],
            {},
        ),
        # FCDO and MOD-DI advice only
        (
            [
                {"id": "advice-1", "level": "user", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                {"id": "advice-2", "level": "team", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                {"id": "advice-3", "level": "user", "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"}},
            ],
            {
                "id-mod-di": [
                    {"id": "advice-3", "level": "user", "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"}},
                ]
            },
        ),
        # All OGDs advising with MOD collected under MOD-ECJU
        (
            [
                {"id": "advice-1", "level": "user", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                {"id": "advice-2", "level": "team", "team": {"alias": FCDO_TEAM, "id": "id-fcdo"}},
                {"id": "advice-3", "level": "team", "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"}},
                {"id": "advice-4", "level": "user", "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"}},
                {"id": "advice-5", "level": "user", "team": {"alias": DESNZ_NUCLEAR, "id": "id-desnz-nuclear"}},
                {"id": "advice-6", "level": "user", "team": {"alias": DESNZ_CHEMICAL, "id": "id-desnz-chemical"}},
                {"id": "advice-7", "level": "user", "team": {"alias": NCSC_TEAM, "id": "id-ncsc"}},
                {"id": "advice-8", "level": "user", "team": {"alias": MOD_CAPPROT_TEAM, "id": "id-mod-capprot"}},
                {"id": "advice-9", "level": "user", "team": {"alias": MOD_DSR_TEAM, "id": "id-mod-dsr"}},
                {"id": "advice-10", "level": "user", "team": {"alias": MOD_DSTL_TEAM, "id": "id-mod-dstl"}},
            ],
            {
                "id-mod-di": [
                    {"id": "advice-4", "level": "user", "team": {"alias": MOD_DI_TEAM, "id": "id-mod-di"}},
                ],
                "id-mod-capprot": [
                    {"id": "advice-8", "level": "user", "team": {"alias": MOD_CAPPROT_TEAM, "id": "id-mod-capprot"}},
                ],
                "id-mod-dsr": [
                    {"id": "advice-9", "level": "user", "team": {"alias": MOD_DSR_TEAM, "id": "id-mod-dsr"}},
                ],
                "id-mod-dstl": [
                    {"id": "advice-10", "level": "user", "team": {"alias": MOD_DSTL_TEAM, "id": "id-mod-dstl"}},
                ],
            },
        ),
    ),
)
def test_get_advice_to_consolidate_mod_ecju(advice, expected_grouping):
    assert get_advice_to_consolidate(advice, MOD_ECJU_TEAM) == expected_grouping
