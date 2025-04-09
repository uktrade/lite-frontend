from django.urls import reverse

from core.application_manifests.base import BaseManifest
from core.application_manifests.registry import application_manifest_registry


@application_manifest_registry.register("CASEWORKER", "application")
class StandardApplicationCaseWorkerManifest(BaseManifest):

    def get_detail_view_url(self, **kwargs):
        return reverse(
            "cases:case",
            kwargs={
                "queue_pk": kwargs["queue_pk"],
                "pk": kwargs["case_id"],
                "tab": "details",
            },
        )


@application_manifest_registry.register("EXPORTER", "application")
class StandardApplicationExporterManifest(BaseManifest):

    def get_detail_view_url(self, **kwargs):
        return
