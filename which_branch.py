import os
import re
import sys

BASE_TARGET_MAP = {
    "dev": "uat",
    "uat": "master",
}

HOTFIX_BRANCH_RE = re.compile("^hotfix-(uat|master)")

DEFAULT_BRANCH = "dev"


class UnknownBranch(Exception):
    pass


def get_current_branch():
    try:
        return os.environ["CIRCLE_BRANCH"]
    except KeyError:
        raise UnknownBranch()


def is_hotfix_branch(branch):
    return bool(HOTFIX_BRANCH_RE.match(branch))


def get_hotfix_target(branch):
    return HOTFIX_BRANCH_RE.match(branch).groups()[0]


def get_presumed_target(branch):
    try:
        return BASE_TARGET_MAP[branch]
    except KeyError:
        pass

    if is_hotfix_branch(branch):
        return get_hotfix_target(branch)

    return DEFAULT_BRANCH


def get_branch(desired_branch):
    if desired_branch != "auto":
        return desired_branch

    try:
        current_branch = get_current_branch()
    except UnknownBranch:
        return "dev"

    presumed_target = get_presumed_target(current_branch)

    return presumed_target


if __name__ == "__main__":
    desired_branch = sys.argv[1]
    print(get_branch(desired_branch))
