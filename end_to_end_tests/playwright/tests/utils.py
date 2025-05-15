import re
from typing import Optional

from playwright.sync_api import Page, expect
from uuid import UUID


def get_application_id(url: str, pattern: str, group_name: str = "app_pk") -> int:
    r"""Parse an application ID from a pattern.

    Example usage:
        >> dfl_id = utils.get_application_id(page.url, r"import/firearms/dfl/(?P<app_pk>\d+)/edit/")
    """

    match: Optional[re.Match] = re.search(re.compile(pattern), url)

    if not match:
        raise ValueError(f"Unable to find pattern {pattern!r} in url: {url}")

    return UUID(match.group(group_name))


def assert_page_url(page: Page, url_pattern: str) -> None:
    """Helper function to check a page url."""

    expected = re.compile(f".*{url_pattern}")

    expect(page).to_have_url(expected)
