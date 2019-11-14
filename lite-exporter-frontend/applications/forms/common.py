from django.urls import reverse_lazy

from lite_content.lite_exporter_frontend import strings
from lite_forms.components import HiddenField, Form, BackLink, TextArea, HTMLBlock, RadioButtons, Option
from lite_forms.generators import confirm_form

from core.builtins.custom_tags import get_string


def respond_to_query_form(application_id, ecju_query):
    return Form(title='Respond to query',
                description='',
                questions=[
                    HTMLBlock('<div class="app-ecju-query__text" style="display: block; max-width: 100%;">' +
                              ecju_query['question'] +
                              '</div><br><br>'),
                    TextArea(name='response',
                             title='Your response',
                             description='You won\'t be able to edit this once you\'ve submitted it.',
                             extras={
                                 'max_length': 2200,
                             }),
                    HiddenField(name='form_name', value='respond_to_query')
                ],
                back_link=BackLink(strings.BACK_TO_APPLICATION, reverse_lazy('applications:detail',
                                                                             kwargs={'pk': application_id,
                                                                                     'type': 'ecju-queries'})),
                default_button_name='Submit response')


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(title='Are you sure you want to send this response?',
                        confirmation_name='confirm_response',
                        hidden_field='ecju_query_response_confirmation',
                        yes_label='Yes, send the response',
                        no_label='No, change my response',
                        back_link_text='Back to edit response',
                        back_url=edit_response_url,
                        submit_button_text='Continue')


def edit_type_form(application_id):
    return Form(title=get_string('applications.edit.title'),
                description=get_string('applications.edit.description'),
                questions=[
                    RadioButtons(name='edit-type',
                                 options=[
                                     Option(key='minor',
                                            value=get_string('applications.edit.minor.title'),
                                            description=get_string('applications.edit.minor.description')),
                                     Option(key='major',
                                            value=get_string('applications.edit.major.title'),
                                            description=get_string('applications.edit.major.description')),
                                 ])],
                back_link=BackLink(strings.BACK_TO_APPLICATION, reverse_lazy('applications:detail',
                                                                             kwargs={'pk': application_id,
                                                                                     'type': 'ecju-queries'})),
                default_button_name='Continue')
