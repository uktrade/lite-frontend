from django.urls import reverse

from core.application_manifests.base import BaseCaseworkerUrls


class F680CaseworkerUrls(BaseCaseworkerUrls):

    @classmethod
    def get_detail_view_url(cls, **kwargs):
        return reverse("cases:f680:details", kwargs={"pk": kwargs["case_id"], "queue_pk": kwargs["queue_pk"]})

    @classmethod
    def get_notes_and_timeline_url(cls, **kwargs):
        return reverse(
            "cases:f680:notes_and_timeline", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["case_id"]}
        )
