from django.urls import reverse

from core.application_manifests.base import BaseCaseworkerUrls


class StandardApplicationCaseworkerUrls(BaseCaseworkerUrls):

    @classmethod
    def get_detail_view_url(cls, **kwargs):
        return reverse(
            "cases:case",
            kwargs={
                "queue_pk": kwargs["queue_pk"],
                "pk": kwargs["case_id"],
                "tab": "details",
            },
        )

    @classmethod
    def get_notes_and_timeline_url(cls, **kwargs):
        return reverse(
            "cases:activities:notes-and-timeline", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["case_id"]}
        )
