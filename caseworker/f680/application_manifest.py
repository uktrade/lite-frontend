from django.urls import reverse

from core.application_manifests.base import BaseManifest
from core.application_manifests.registry import application_manifest_registry


@application_manifest_registry.register("CASEWORKER", "security_clearance")
class F680CaseWorkerManifest(BaseManifest):

    def get_detail_view_url(self, **kwargs):
        return reverse("cases:f680:details", kwargs={"pk": kwargs["case_id"], "queue_pk": kwargs["queue_pk"]})


@application_manifest_registry.register("EXPORTER", "security_clearance")
class F680ExporterManifest(BaseManifest):

    def get_detail_view_url(self, **kwargs):
        return
