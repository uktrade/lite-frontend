from django.http import HttpRequest
from django.urls import reverse

from lite_content.lite_internal_frontend.cases import Manage
from lite_forms.components import Form, Checkboxes, Filter, BackLink
from queues.services import get_queues


def move_case_form(request: HttpRequest, queue, case: dict):
    return Form(
        Manage.MoveCase.TITLE,
        Manage.MoveCase.DESCRIPTION,
        [Filter(), Checkboxes("queues[]", get_queues(request, convert_to_options=True), filterable=True)],
        back_link=BackLink(url=reverse("cases:case", kwargs={"queue_pk": queue["id"], "pk": case["id"]})),
        container="case",
    )
