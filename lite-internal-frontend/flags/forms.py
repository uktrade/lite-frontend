from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType, ArrayQuestion, HelpSection, Option


def add_flag_form():
    return Form(title='Add Flag', description='', questions=[
            Question(title='Name',
                     description='',
                     input_type=InputType.INPUT,
                     name='name'),
            ArrayQuestion(title='Level',
                          description='',
                          input_type=InputType.SELECT,
                          name='level',
                          data=[Option('Case', 'Case'),
                                Option('Organisation', 'Organisation'),
                                Option('Destination', 'Destination'),
                                Option('Good', 'Good')])
        ])


def edit_flag_form():
    return Form(title='Edit Flag', description='', caption='', questions=[
            Question(title='Name',
                     description='',
                     input_type=InputType.INPUT,
                     name='name'),
            ArrayQuestion(title='Level',
                          description='',
                          input_type=InputType.SELECT,
                          name='level',
                          data=[Option('Case', 'Case'),
                                Option('Organisation', 'Organisation'),
                                Option('Destination', 'Destination'),
                                Option('Good', 'Good')])
        ])
