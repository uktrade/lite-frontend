import pytest
import re

from bs4 import BeautifulSoup

from django.urls import reverse
from core import client


@pytest.fixture
def url(data_standard_case):
    return reverse(
        "applications:application",
        kwargs={
            "pk": data_standard_case["case"]["id"],
            "type": "ecju-queries",
        },
    )


@pytest.fixture(autouse=True)
def application_url(requests_mock, data_standard_case):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    requests_mock.get(url=app_url, json=data_standard_case["case"]["data"])


@pytest.fixture(autouse=True)
def mock_ecju_queries(data_standard_case, data_ecju_queries, requests_mock):
    requests_mock.get(
        re.compile(
            rf"/cases/{data_standard_case['case']['id']}/ecju-queries",
        ),
        json=data_ecju_queries,
    )


@pytest.fixture()
def rendered_ecju_queries(authorized_client, url):
    response = authorized_client.get(url)
    return BeautifulSoup(response.content, "html.parser").find_all(id="open-ecju-query")


def test_renders_team_name(rendered_ecju_queries):
    assert rendered_ecju_queries[0].p.get_text() == "BEIS CWC"


def test_shortens_beis_chemical_team_name(rendered_ecju_queries):
    assert rendered_ecju_queries[1].p.get_text() == "BEIS"


def test_shortens_beis_nuclear_team_name(rendered_ecju_queries):
    assert rendered_ecju_queries[2].p.get_text() == "BEIS Nuclear"
