from lite_content.lite_internal_frontend.strings import cases
from django.http import HttpRequest
from lite_forms.components import Form, Checkboxes, Filter, BackLink

from queues.services import get_queues


def move_case_form(request: HttpRequest, case_url: str):
    return Form(
        cases.Manage.MoveCase.TITLE,
        cases.Manage.MoveCase.DESCRIPTION,
        [Filter(), Checkboxes("queues", get_queues(request, True)),],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        back_link=BackLink("Back to Case", case_url),
    )
