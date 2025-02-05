from django.urls import reverse

from core.summaries.summaries import (
    f680_goods_summary,
    f680_good_details_on_application_summary as core_f680_good_details_on_application_summary,
)


def get_complete_item_summary_edit_link_factory(application, good):
    def get_edit_link(name):
        return reverse(
            f"applications:complete_item_edit_{name}",
            kwargs={
                "pk": application["id"],
                "good_pk": good["id"],
            },
        )

    return get_edit_link


def f680_good_details_summary(good, *args, **kwargs):

    return f680_goods_summary(good)


def f680_good_details_on_application_summary(good_on_application, *args, **kwargs):
    return core_f680_good_details_on_application_summary(good_on_application)
