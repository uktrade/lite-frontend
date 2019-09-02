from django.urls import reverse_lazy

from core.builtins.custom_tags import get_string
from lite_forms.components import RadioButtons, Form, Option, TextArea, Select, TextInput, FormGroup, FileUpload, \
    BackLink, Label
from lite_forms.generators import confirm_form
from core.services import get_countries


def new_end_user_forms():
    return FormGroup([
        Form(title='Who will be the final recipient (end-user) of your goods?',
             questions=[
                 RadioButtons('type',
                              options=[
                                  Option('government', 'A Government Organisation'),
                                  Option('commercial', 'A Commercial Organisation'),
                                  Option('individual', 'An Individual'),
                                  Option('other', 'Other', show_or=True),
                              ]),
             ],
             default_button_name='Continue'),
        Form(title='Enter the final recipient\'s name',
             questions=[
                 TextInput('name'),
             ],
             default_button_name='Continue'),
        Form(title='Enter the final recipient\'s web address (URL)',
             questions=[
                 TextInput('website', optional=True),
             ],
             default_button_name='Continue'),
        Form(title='Where\'s the final recipient based?',
             questions=[
                 TextArea('address', 'Address'),
                 Select(title='Country',
                        name='country',
                        options=get_countries(None, True)),
             ],
             default_button_name='Save and continue')
    ])


def attach_document_form(draft_url):
    return Form(get_string('end_user.documents.attach_documents.title'),
                get_string('end_user.documents.attach_documents.description'),
                [FileUpload('documents')],
                back_link=BackLink(get_string('end_user.documents.attach_documents.back_to_application_overview'),
                                   draft_url),
                footer_label=Label('Or <a href="'
                                   + draft_url
                                   + '" class="govuk-link govuk-link--no-visited-state">'
                                   + get_string('end_user.documents.save_end_user')
                                   + '</a> ' + get_string('end_user.documents.attach_later')))


def delete_document_confirmation_form(overview_url):
    return confirm_form(title='Are you sure you want to delete this document?',
                        confirmation_name='delete_document_confirmation',
                        back_link_text=get_string('end_user.documents.attach_documents.back_to_application_overview'),
                        back_url=overview_url
                        )
