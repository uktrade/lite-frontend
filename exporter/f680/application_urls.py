from django.urls import reverse
from core.application_manifests.base import BaseExporterUrls


class F680ExporterUrls(BaseExporterUrls):

    @classmethod
    def get_application_detail_url(cls, **kwargs):
        return reverse("f680:submitted_summary", kwargs={"pk": kwargs["pk"]})

    @classmethod
    def get_application_task_list_url(cls, **kwargs):
        return reverse("f680:summary", kwargs={"pk": kwargs["pk"]})
