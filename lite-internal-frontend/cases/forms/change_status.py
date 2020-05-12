from django.urls import reverse

from lite_content.lite_internal_frontend import cases
from lite_forms.components import Form, Option, Select, BackLink


def change_status_form(queue, case, statuses):
    return Form(
        title=cases.ChangeStatusPage.TITLE,
        description=cases.ChangeStatusPage.DESCRIPTION,
        questions=[
            Select(
                name="status",
                options=[Option(status["key"], status["value"]) for status in statuses],
                include_default_select=False,
            )
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue["id"], "pk": case["id"]})),
        container="case",
    )
