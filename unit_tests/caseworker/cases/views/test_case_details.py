import pytest

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from caseworker.cases.helpers.case import LU_POST_CIRC_FINALISE_QUEUE_ALIAS


@pytest.fixture(autouse=True)
def setup(
    settings,
    mock_queue,
    mock_gov_lu_user,
    mock_case,
    mock_standard_case_activity_filters,
    mock_standard_case_activity_system_user,
    mock_standard_case_ecju_queries,
    mock_standard_case_assigned_queues,
    mock_standard_case_documents,
    mock_standard_case_additional_contacts,
    mock_standard_case_on_post_circulation_queue,
):
    pass


def test_case_details_im_done_lu_user(authorized_client, data_queue, data_standard_case):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["hide_im_done"] == True
    assert context["current_user"]["team"]["alias"] == "LICENSING_UNIT"
    assert len(context["case"]["queue_details"]) == 1
    assert context["case"]["queue_details"][0]["alias"] == LU_POST_CIRC_FINALISE_QUEUE_ALIAS


def test_case_details_im_done_fcdo_user(
    authorized_client,
    data_queue,
    data_standard_case,
    mock_standard_case_on_fcdo_countersigning_queue,
    mock_gov_fcdo_user,
):
    url = reverse("cases:case", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]})
    response = authorized_client.get(url)
    assertTemplateUsed(response, "layouts/case.html")
    context = response.context
    assert context["hide_im_done"] == False
    assert context["current_user"]["team"]["alias"] == "FCDO"
    assert len(context["case"]["queue_details"]) == 1
    assert context["case"]["queue_details"][0]["alias"] == "FCDO_COUNTER_SIGNING"
