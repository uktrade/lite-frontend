import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from caseworker.cases.objects import Case


@pytest.fixture(autouse=True)
def setup(
    settings,
    mock_queue,
    mock_gov_user,
    mock_case,
    mock_standard_case_activity_system_user,
):
    settings.FEATURE_FLAG_NOTES_TIMELINE_2_0 = True


@pytest.fixture
def notes_and_timelines_all_url(data_queue, data_standard_case):
    return reverse(
        "cases:activities:notes-and-timeline-all",
        kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]},
    )


def test_notes_and_timelines_all_view_flag_off_status_code(
    settings,
    authorized_client,
    notes_and_timelines_all_url,
):
    settings.FEATURE_FLAG_NOTES_TIMELINE_2_0 = False
    response = authorized_client.get(notes_and_timelines_all_url)
    assert response.status_code == 404


def test_notes_and_timelines_all_view_flag_on_status_code(
    authorized_client,
    notes_and_timelines_all_url,
):
    response = authorized_client.get(notes_and_timelines_all_url)
    assert response.status_code == 200


def test_notes_and_timelines_all_view_templates(
    authorized_client,
    notes_and_timelines_all_url,
):
    response = authorized_client.get(notes_and_timelines_all_url)
    assertTemplateUsed(response, "activities/notes-and-timeline-all.html")
    assertTemplateUsed(response, "layouts/case.html")
    assertTemplateUsed(response, "includes/case-tabs.html")


def test_notes_and_timelines_context_data(
    authorized_client,
    notes_and_timelines_all_url,
    data_standard_case,
    standard_case_activity,
):
    response = authorized_client.get(notes_and_timelines_all_url)
    assert response.context["case"] == Case(data_standard_case["case"])
    assert response.context["activities"] == standard_case_activity["activity"]
