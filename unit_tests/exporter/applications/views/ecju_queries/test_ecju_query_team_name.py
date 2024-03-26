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


@pytest.fixture()
def rendered_ecju_closed_queries(authorized_client, url):
    response = authorized_client.get(url)
    return BeautifulSoup(response.content, "html.parser").find_all(id="closed-ecju-query")


@pytest.fixture()
def rendered_ecju_queries(authorized_client, url):
    response = authorized_client.get(url)
    return BeautifulSoup(response.content, "html.parser").find_all(id="open-ecju-query")


def test_renders_team_name(rendered_ecju_queries):
    assert rendered_ecju_queries[0].p.get_text() == "DESNZ Chemical"


def test_shortens_desnz_chemical_team_name(rendered_ecju_queries):
    assert rendered_ecju_queries[1].p.get_text() == "DESNZ Chemical"


def test_shortens_desnz_nuclear_team_name(rendered_ecju_queries):
    assert rendered_ecju_queries[2].p.get_text() == "DESNZ Nuclear"


def test_renders_is_manually_closed_query(rendered_ecju_closed_queries):
    rendered_item = rendered_ecju_closed_queries[0].find(class_="app-ecju-query__item")
    manually_closed_text = rendered_item.find_all("p")[3].text.replace("\n", "").replace("\t", "").strip()

    assert "This query was closed by the case worker at 5:00pm on 30 November 2022." in manually_closed_text


def test_renders_is_manually_closed_query_not_visible(rendered_ecju_closed_queries):

    rendered_item = rendered_ecju_closed_queries[1].find(class_="app-ecju-query__item--right")
    assert rendered_item.find_all("p")[1].get_text() == "query is closed non-manually"
    assert (
        rendered_ecju_closed_queries[1].find(
            text="This query was closed by the case worker at 5:00pm on 30 November 2022."
        )
        is None
    )
