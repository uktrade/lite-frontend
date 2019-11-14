from django.urls import reverse_lazy

from lite_content.lite_internal_frontend import strings
from lite_forms.components import Form, Select, TextInput, BackLink

from core.builtins.custom_tags import get_string
from lite_forms.helpers import conditional
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


def edit_user_form(request, user_id, super_user):
    return Form(title='Edit User',
                questions=[
                    TextInput(title='Email',
                              name='email'),
                    Select(name='team',
                           title='What team will the user belong to?',
                           options=get_teams(request, True)),
                    conditional(not super_user, Select(name='role',
                                                       options=get_roles(request, True),
                                                       title=strings.USER_ROLE_QUESTION), )
                ],
                back_link=BackLink('Back to User', reverse_lazy('users:user', kwargs={'pk': user_id})),
                default_button_name='Save')
