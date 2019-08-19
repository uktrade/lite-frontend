from django.http import HttpRequest
from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType, Checkboxes, BackLink
from users.services import get_permissions


def add_role(request: HttpRequest):
    return Form(title=get_string('roles.add.title'),
                description=get_string('roles.add.description'),
                questions=[
            Question(title='What do you want to call the role?',
                     description='',
                     input_type=InputType.INPUT,
                     name='name'),
            Checkboxes(name='permissions',
                       options=get_permissions(request, True),
                       title='What permissions should this role have?',
                       description='Select all permissions that apply.'),
        ],
                back_link=BackLink('Back to Roles', reverse_lazy('users:roles')),
                default_button_name='Create')


def edit_role(request: HttpRequest):
    return Form(title=get_string('roles.edit.title'),
                description=get_string('roles.edit.description'),
                questions=[
            Question(title='What do you want to call the role?',
                     description='',
                     input_type=InputType.INPUT,
                     name='name'),
            Checkboxes(name='permissions',
                       options=get_permissions(request, True),
                       title='What permissions should this role have?',
                       description='Select all permissions that apply.'),
        ],
                back_link=BackLink('Back to Roles', reverse_lazy('users:roles')),
                default_button_name='Save')
