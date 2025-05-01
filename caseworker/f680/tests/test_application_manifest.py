from django.urls import reverse

from core.application_manifests.helpers import get_caseworker_manifest_for_application_reference
from caseworker.cases.objects import Case


def test_get_url_from_f680_manifest_via_application_reference():
    manifest = get_caseworker_manifest_for_application_reference("F680/2025/0000001")
    assert manifest.urls.get_detail_view_url(
        case_id="11111111-1111-1111-1111-111111111111",
        queue_pk="22222222-2222-2222-2222-222222222222",
    ) == reverse(
        "cases:f680:details",
        kwargs={
            "pk": "11111111-1111-1111-1111-111111111111",
            "queue_pk": "22222222-2222-2222-2222-222222222222",
        },
    )


def test_get_url_from_f680_manifest_via_case(data_submitted_f680_case):
    case = Case(data_submitted_f680_case["case"])
    assert case.manifest.urls.get_notes_and_timeline_url(
        case_id="11111111-1111-1111-1111-111111111111",
        queue_pk="22222222-2222-2222-2222-222222222222",
    ) == reverse(
        "cases:f680:notes_and_timeline",
        kwargs={
            "pk": "11111111-1111-1111-1111-111111111111",
            "queue_pk": "22222222-2222-2222-2222-222222222222",
        },
    )
