from lite_content.lite_internal_frontend import strings
from django.http import HttpRequest
from lite_forms.components import Form, Checkboxes, Filter, BackLink

from queues.services import get_queues


def move_case_form(request: HttpRequest, case_url: str):
    return Form(
        strings.Cases.Manage.MoveCase.TITLE,
        strings.Cases.Manage.MoveCase.DESCRIPTION,
        [Filter(), Checkboxes("queues", get_queues(request, True)),],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        back_link=BackLink("Back to Case", case_url),
    )
