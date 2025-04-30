from django.urls import reverse

from core.application_manifests.helpers import (
    get_exporter_manifest_for_application,
    get_exporter_manifest_for_application_reference,
)
from exporter.core.objects import Application


def test_get_url_from_f680_manifest_via_application_reference():
    manifest = get_exporter_manifest_for_application_reference("F680/2025/0000001")
    assert manifest.urls.get_application_detail_url(
        pk="11111111-1111-1111-1111-111111111111",
    ) == reverse(
        "f680:submitted_summary",
        kwargs={
            "pk": "11111111-1111-1111-1111-111111111111",
        },
    )


def test_get_url_from_f680_manifest_via_application(data_f680_submitted_application):
    application = Application(data_f680_submitted_application)
    manifest = get_exporter_manifest_for_application(application)
    assert manifest.urls.get_application_task_list_url(
        pk="22222222-2222-2222-2222-222222222222",
    ) == reverse(
        "f680:summary",
        kwargs={
            "pk": "22222222-2222-2222-2222-222222222222",
        },
    )
