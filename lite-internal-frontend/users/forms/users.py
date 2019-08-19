from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType, Select, BackLink
from teams.services import get_teams
from users.services import get_roles


def add_user_form(request):
    return Form(title=get_string('users.invite'),
                description='',
                questions=[
                    Question(title='What\'s the user\'s email?',
                             description='',
                             input_type=InputType.INPUT,
                             name='email'),
                    Select(name='team',
                           title='What team will the user belong to?',
                           options=get_teams(request, True)),
                    Select(name='role',
                           options=get_roles(request, True),
                           title='What role should this user have?'),
                ],
                back_link=BackLink('Back to Users', reverse_lazy('users:users')))


def edit_user_form(request):
    return Form(title='Edit User',
                description='',
                caption='',
                questions=[
                    Question(title='Email',
                             description='',
                             input_type=InputType.INPUT,
                             name='email'),
                    Select(name='team',
                           title='What team will the user belong to?',
                           options=get_teams(request, True)),
                    Select(name='role',
                           options=get_roles(request, True),
                           title='What role should this user have?'),
                ],
                back_link=BackLink('Back to Users', reverse_lazy('users:users')),
                default_button_name='Save')
