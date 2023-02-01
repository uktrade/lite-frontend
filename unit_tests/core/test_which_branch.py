import os
import pytest

from which_branch import get_branch


@pytest.mark.parametrize(
    "circle_branch, expected_target",
    (
        ("dev", "uat"),
        ("uat", "master"),
        ("LTD-1234-ticket", "dev"),
        ("random-branch-name", "dev"),
        ("hotfix-master", "master"),
        ("hotfix-uat", "uat"),
        ("hotfix-master-fix-for-this-thing", "master"),
        ("hotfix-uat-fix-for-that-thing", "uat"),
    ),
)
def test_get_branch_auto(circle_branch, expected_target, mocker):
    mocker.patch.dict(os.environ, {"CIRCLE_BRANCH": circle_branch})
    assert get_branch("auto") == expected_target


def test_get_branch_auto_without_env_var(mocker):
    mocker.patch.dict("os.environ")
    os.environ.pop("CIRCLE_BRANCH", None)
    assert get_branch("auto") == "dev"


@pytest.mark.parametrize(
    "circle_branch",
    (
        "dev",
        "uat",
        "LTD-1234-ticket",
        "random-branch-name",
        "hotfix-master-fix-for-thing",
        "hotfix-uat-fix-another-thing",
    ),
)
def test_get_branch_explicit(circle_branch, mocker):
    mocker.patch.dict(os.environ, {"CIRCLE_BRANCH": circle_branch})
    assert get_branch("explicit-branch-name") == "explicit-branch-name"
