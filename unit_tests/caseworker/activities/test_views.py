import pytest

from django.urls import reverse


@pytest.fixture(autouse=True)
def setup(settings):
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
    mock_queue,
    mock_gov_user,
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
