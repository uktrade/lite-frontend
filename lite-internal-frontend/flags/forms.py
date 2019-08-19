from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType, Option, Select, BackLink

_name = Question(title='Name',
                 description='',
                 input_type=InputType.INPUT,
                 name='name')

_level = Select(name='level',
                options=[Option('Case', 'Case'),
                         Option('Organisation', 'Organisation'),
                         Option('Destination', 'Destination'),
                         Option('Good', 'Good')],
                title='Level')

_back_link = BackLink('Back to Flags', reverse_lazy('flags:flags'))


def add_flag_form():
    return Form(title=get_string('flags.create'),
                description='',
                questions=[
                    _name,
                    _level,
                ],
                back_link=_back_link,
                default_button_name='Create')


def edit_flag_form():
    return Form(title='Edit Flag',
                description='',
                questions=[
                    _name,
                    _level,
                ],
                back_link=_back_link,
                default_button_name='Save')
