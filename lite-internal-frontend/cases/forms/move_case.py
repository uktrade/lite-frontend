from django.http import HttpRequest

from cases.helpers import case_view_breadcrumbs
from lite_content.lite_internal_frontend.cases import Manage
from lite_forms.components import Form, Checkboxes, Filter
from queues.services import get_queues


def move_case_form(request: HttpRequest, queue, case: dict):
    return Form(
        Manage.MoveCase.TITLE,
        Manage.MoveCase.DESCRIPTION,
        [Filter(), Checkboxes("queues[]", get_queues(request, True)),],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        back_link=case_view_breadcrumbs(queue, case, Manage.MoveCase.TITLE),
    )
