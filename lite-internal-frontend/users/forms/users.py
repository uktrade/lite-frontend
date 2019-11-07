from django.urls import reverse_lazy
from lite_forms.components import Form, Select, TextInput, BackLink

from core.builtins.custom_tags import get_string
from teams.services import get_teams
from users.services import get_roles


def add_user_form(request):
    return Form(title=get_string('users.invite'),
                questions=[
                    TextInput(title='What\'s the user\'s email?',
                              name='email'),
                    Select(name='team',
                           title='What team will the user belong to?',
                           options=get_teams(request, True)),
                    Select(name='role',
                           options=get_roles(request, True),
                           title='What role should this user have?'),
                ],
                back_link=BackLink('Back to Users', reverse_lazy('users:users')))


def edit_user_form(request, user_id):
    return Form(title='Edit User',
                description='',
                caption='',
                questions=[
                    TextInput(title='Email',
                              name='email'),
                    Select(name='team',
                           title='What team will the user belong to?',
                           options=get_teams(request, True)),
                    Select(name='role',
                           options=get_roles(request, True),
                           title='What role should this user have?'),
                ],
                back_link=BackLink('Back to User', reverse_lazy('users:user', kwargs={'pk': user_id})),
                default_button_name='Save')
