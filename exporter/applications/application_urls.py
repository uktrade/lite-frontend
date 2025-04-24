from django.urls import reverse
from core.application_manifests.base import BaseExporterUrls


class StandardApplicationExporterUrls(BaseExporterUrls):

    @classmethod
    def get_application_detail_url(cls, **kwargs):
        return reverse("applications:application", kwargs={"pk": kwargs["pk"]})

    @classmethod
    def get_application_task_list_url(cls, **kwargs):
        return reverse("applications:task_list", kwargs={"pk": kwargs["pk"]})
