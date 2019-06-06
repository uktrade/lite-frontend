from core.services import get_denial_reasons
from libraries.forms.components import Question, Form, InputType


def denial_reasons_form():
    form = Form('Why do you want to deny this application?', 'Select all that apply.', get_denial_reasons(None),
                default_button_name='Submit')

    form.questions.append(Question('Add any additional information to support your denial',
                                   '',
                                   InputType.TEXTAREA,
                                   'reason_details',
                                   optional=True))

    return form
