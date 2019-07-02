from core.builtins.custom_tags import get_string
from core.services import get_queues
from libraries.forms.components import Form, Filter, Checkboxes


def move_case_form(request):
    return Form(get_string('cases.manage.move_case.title'),
                get_string('cases.manage.move_case.description'),
                [
                    Filter(),
                    Checkboxes('queues', get_queues(request, True)),
                ],
                javascript_imports=['/assets/javascripts/filter-checkbox-list.js'])
