from django.http import HttpRequest
from django.urls import reverse

from lite_content.lite_internal_frontend.cases import Manage
from lite_forms.components import Form, Checkboxes, Filter, BackLink, DetailComponent, TextArea
from caseworker.queues.services import get_queues


def move_case_form(request: HttpRequest, queue, case: dict):
    return Form(
        title=Manage.MoveCase.TITLE,
        description=Manage.MoveCase.DESCRIPTION,
        questions=[
            Filter(),
            Checkboxes("queues[]", get_queues(request, convert_to_options=True), filterable=True),
            DetailComponent(
                title=Manage.MoveCase.NOTE,
                components=[
                    TextArea(name="note", classes=["govuk-!-margin-0"]),
                ],
            ),
        ],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue["id"], "pk": case["id"]})),
        container="case",
    )
