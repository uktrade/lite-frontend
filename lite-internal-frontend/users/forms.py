from core.builtins.custom_tags import get_string
from libraries.forms.components import Question, Form, InputType, ArrayQuestion, HelpSection


def add_user_form(teams):
    return Form(title=get_string('users.invite'), description='', questions=[
            Question(title='What\'s the user\'s email?',
                     description='',
                     input_type=InputType.INPUT,
                     name='email'),
            ArrayQuestion(title='What team will the user belong to?',
                          description='',
                          input_type=InputType.SELECT,
                          name='team',
                          data=teams),
        ])


def edit_user_form(teams):
    return Form(title='Edit User', description='', caption='', questions=[
            Question(title='Email',
                     description='',
                     input_type=InputType.INPUT,
                     name='email'),
            ArrayQuestion(title='Team',
                          description='',
                          input_type=InputType.SELECT,
                          name='team',
                          data=teams),
        ])
