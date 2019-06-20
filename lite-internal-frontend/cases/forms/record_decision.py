from core.builtins.custom_tags import get_string
from libraries.forms.components import Form, InputType, ArrayQuestion, Option


def record_decision_form():
    return Form(get_string('cases.record_decision.title'),
                '',
                [
                    ArrayQuestion('',
                                  '',
                                  InputType.RADIOBUTTONS,
                                  'status',
                                  [
                                      Option('approved', get_string('cases.record_decision.grant')),
                                      Option('declined', get_string('cases.record_decision.deny'))
                                  ])
                ],
                default_button_name='Submit')
