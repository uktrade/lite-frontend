import pytest
import rules

from exporter.goods.constants import GoodStatus


@pytest.mark.parametrize(
    "status, expected",
    (
        ({"key": GoodStatus.DRAFT, "value": GoodStatus.DRAFT.title()}, True),
        ({"key": GoodStatus.SUBMITTED, "value": GoodStatus.SUBMITTED.title()}, False),
        ({"key": GoodStatus.VERIFIED, "value": GoodStatus.VERIFIED.title()}, False),
    ),
)
def test_can_user_delete_product_predicates(settings, rf, data_standard_case, status, expected):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    good["status"] = status

    request = rf.get("/")
    assert rules.test_rule("can_delete_product", request, good) is expected


@pytest.mark.parametrize(
    "status, is_archived, expected",
    (
        ({"key": GoodStatus.DRAFT, "value": GoodStatus.DRAFT.title()}, False, False),
        ({"key": GoodStatus.SUBMITTED, "value": GoodStatus.SUBMITTED.title()}, False, True),
        ({"key": GoodStatus.VERIFIED, "value": GoodStatus.VERIFIED.title()}, False, True),
        ({"key": GoodStatus.SUBMITTED, "value": GoodStatus.SUBMITTED.title()}, True, False),
        ({"key": GoodStatus.VERIFIED, "value": GoodStatus.VERIFIED.title()}, True, False),
    ),
)
def test_can_user_archive_product_predicates(settings, rf, data_standard_case, status, is_archived, expected):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    good["status"] = status
    good["is_archived"] = is_archived

    request = rf.get("/")
    assert rules.test_rule("can_archive_product", request, good) is expected


@pytest.mark.parametrize(
    "status, is_archived, expected",
    (
        ({"key": GoodStatus.DRAFT, "value": GoodStatus.DRAFT.title()}, False, False),
        ({"key": GoodStatus.SUBMITTED, "value": GoodStatus.SUBMITTED.title()}, False, False),
        ({"key": GoodStatus.VERIFIED, "value": GoodStatus.VERIFIED.title()}, False, False),
        ({"key": GoodStatus.SUBMITTED, "value": GoodStatus.SUBMITTED.title()}, True, True),
        ({"key": GoodStatus.VERIFIED, "value": GoodStatus.VERIFIED.title()}, True, True),
    ),
)
def test_can_user_restore_product_predicates(settings, rf, data_standard_case, status, is_archived, expected):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    good["status"] = status
    good["is_archived"] = is_archived

    request = rf.get("/")
    assert rules.test_rule("can_restore_product", request, good) is expected
