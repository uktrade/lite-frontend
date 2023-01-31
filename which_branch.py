import os
import re
import sys


def get_current_branch():
    return os.environ.get("CIRCLE_BRANCH", "dev")


BASE_TARGET_MAP = {
    "dev": "uat",
    "uat": "master",
}


HOTFIX_BRANCH_RE = re.compile("^hotfix-(.*)-.*$")


def is_hotfix_branch(branch):
    return bool(HOTFIX_BRANCH_RE.match(branch))


def get_hotfix_target(branch):
    return HOTFIX_BRANCH_RE.match(branch).groups()[0]


DEFAULT_BRANCH = "dev"


def get_presumed_target(branch):
    try:
        return BASE_TARGET_MAP[branch]
    except KeyError:
        pass

    if is_hotfix_branch(branch):
        return get_hotfix_target(branch)

    return DEFAULT_BRANCH


def get_branch():
    _, desired_branch, *_ = sys.argv
    if desired_branch != "auto":
        return desired_branch

    current_branch = get_current_branch()
    presumed_target = get_presumed_target(current_branch)

    return presumed_target


if __name__ == "__main__":
    print(get_branch())
