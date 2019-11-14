from django.urls import reverse_lazy

from applications.components import back_to_task_list
from core.builtins.custom_tags import get_string
from core.services import get_countries
from lite_forms.common import country_question
from lite_forms.components import RadioButtons, Form, Option, TextArea, TextInput, FormGroup, FileUpload, \
    Label
from lite_forms.generators import confirm_form


def third_parties_standard_form(application, opening_title=None):
    return [
        Form(title=opening_title,
             questions=[
                 RadioButtons('sub_type',
                              options=[
                                  Option('government', 'A Government Organisation'),
                                  Option('commercial', 'A Commercial Organisation'),
                                  Option('individual', 'An Individual'),
                                  Option('other', 'Other', show_or=True),
                              ]),
             ],
             default_button_name='Continue',
             back_link=back_to_task_list(application['id'])),
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
                 country_question(countries=get_countries(None, True),
                                  prefix='')
             ],
             default_button_name='Save and continue')
    ]


def new_end_user_forms(application):
    return FormGroup(third_parties_standard_form(application, get_string('end_user.title')))


def attach_document_form(application_id, title, return_later_text, description_text=None):
    inputs = [FileUpload('documents')]
    if description_text:
        inputs.append(TextArea(title=description_text,
                               optional=True,
                               name='description',
                               extras={
                                   'max_length': 280,
                               }))
    return Form(title,
                get_string('end_user.documents.attach_documents.description'),
                inputs,
                back_link=back_to_task_list(application_id),
                footer_label=Label('Or <a href="'
                                   + str(reverse_lazy('applications:task_list', kwargs={'pk': application_id}))
                                   + '" class="govuk-link govuk-link--no-visited-state">'
                                   + return_later_text
                                   + '</a> ' + get_string('end_user.documents.attach_later')))


def delete_document_confirmation_form(overview_url, back_link_text):
    return confirm_form(title='Are you sure you want to delete this document?',
                        confirmation_name='delete_document_confirmation',
                        back_link_text=back_link_text,
                        back_url=overview_url
                        )


def new_consignee_forms(application):
    return FormGroup(third_parties_standard_form(application, get_string('consignee.title')))
