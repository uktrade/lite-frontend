from lite_forms.components import Form, TextArea

from core.services import get_denial_reasons


def denial_reasons_form():
    form = Form('Why do you want to deny this application?', 'Select all that apply.', get_denial_reasons(None),
                default_button_name='Submit')

    form.questions.append(TextArea(title='Add any additional information to support your denial',
                                   name='reason_details',
                                   optional=True))

    return form
