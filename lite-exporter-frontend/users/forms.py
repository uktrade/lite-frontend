from django.urls import reverse_lazy
from lite_forms.components import TextInput, Form, BackLink

_questions = [
    TextInput(title='First name',
              name='first_name'),
    TextInput(title='Last name',
              name='last_name'),
    TextInput(title='Email',
              name='email'),
]

_back_link = BackLink('Back to Users', reverse_lazy('users:users'))

form = Form(title='Add a member to your organisation',
            description='',
            questions=_questions,
            back_link=_back_link)

edit_form = Form(title='Edit member',
                 description='',
                 questions=_questions,
                 back_link=_back_link)
