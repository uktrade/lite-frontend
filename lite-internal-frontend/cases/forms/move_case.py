from core.builtins.custom_tags import get_string
from core.services import get_queues
from libraries.forms.components import Form, ArrayQuestion, InputType, Filter


def move_case_form(request):
    return Form(get_string('cases.manage.move_case.title'),
                get_string('cases.manage.move_case.description'),
                [
                    Filter(),
                    ArrayQuestion('', '', InputType.CHECKBOXES, 'queues', get_queues(request, True))
                ],
                default_button_name='Submit',
                javascript_imports=['/assets/javascripts/filter-checkbox-list.js'])
