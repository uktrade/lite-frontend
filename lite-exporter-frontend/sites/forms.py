from django.urls import reverse_lazy
from lite_forms.common import address_questions
from lite_forms.components import Heading, BackLink, Form, TextInput
from lite_forms.styles import HeadingStyle

from core.builtins.custom_tags import get_string
from core.services import get_countries


def new_site_form():
    return Form(title=get_string('sites.create'),
                description='',
                questions=[
                    TextInput(title='Name of site',
                              name='name'),
                    Heading('Where is the site based?', HeadingStyle.M),
                    *address_questions(get_countries(None, True)),
                ],
                back_link=BackLink('Back to Sites', reverse_lazy('sites:sites')))


def edit_site_form(title):
    return Form(title=title,
                questions=[
                    TextInput(title='Name of site',
                              name='name'),
                    Heading('Where is the site based?', HeadingStyle.M),
                    *address_questions(get_countries(None, True)),
                ],
                back_link=BackLink('Back to Sites', reverse_lazy('sites:sites')))
