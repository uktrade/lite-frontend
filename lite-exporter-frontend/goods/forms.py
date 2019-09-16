from django.urls import reverse, reverse_lazy
from lite_forms.components import Form, TextArea, RadioButtons, Option, BackLink, FileUpload, TextInput, HTMLBlock, \
    HiddenField, Button, Summary
from lite_forms.generators import confirm_form
from lite_forms.styles import ButtonStyle

from conf.settings import env
from core.builtins.custom_tags import get_string
from goods.helpers import good_summary

add_goods_questions = Form(title='Add Good', description='', caption='', questions=[
    TextArea(title='Description of good',
             description='This can make it easier to find your good later',
             name='description',
             extras={
                 'max_length': 280,
             }),
    RadioButtons(title='Is your good controlled?',
                 description='If you don\'t know you can use <a class="govuk-link" href="' + env(
                     'PERMISSIONS_FINDER_URL') + '">Permissions Finder</a>.',
                 name='is_good_controlled',
                 options=[
                     Option(key='yes',
                            value='Yes',
                            show_pane='pane_control_code'),
                     Option(key='no',
                            value='No'),
                     Option(key='unsure',
                            value='I don\'t know')
                 ],
                 classes=['govuk-radios--inline']),
    TextInput(title='What\'s your good\'s control list entry?',
              description='<noscript>If your good is controlled, enter its control list entry. </noscript>For example, ML1a.',
              name='control_code'),
    RadioButtons(title='Is your good intended to be incorporated into an end product?',
                 description='',
                 name='is_good_end_product',
                 options=[
                     Option(key='no',
                            value='Yes'),
                     Option(key='yes',
                            value='No')
                 ],
                 classes=['govuk-radios--inline']),
    TextInput(title='Part Number',
              name='part_number',
              optional=True),
])


def are_you_sure(good_id):
    return Form(title=get_string('clc.clc_form.title'),
                description=get_string('clc.clc_form.description'),
                questions=[
                    TextInput(
                        title='What do you think is your good\'s control list entry?',
                        description='For example, ML1a.',
                        name='not_sure_details_control_code'),
                    TextArea(
                        title='Further details about your goods',
                        description='Please enter details of why you don\'t know if your good is controlled',
                        optional=True,
                        name='not_sure_details_details'),
                ],
                back_link=BackLink('Back to good', reverse('goods:good',
                                                           kwargs={'pk': good_id}))
                )


def edit_form(good_id):
    return Form(title='Edit Good', questions=[
        TextArea(title='Description of good',
                 description='This can make it easier to find your good later',
                 name='description',
                 extras={
                     'max_length': 280,
                 }),
        RadioButtons(title='Is your good controlled?',
                     description='If you don\'t know you can use <a class="govuk-link" href="' + env(
                         'PERMISSIONS_FINDER_URL') + '">Permissions Finder</a>.',
                     name='is_good_controlled',
                     options=[
                         Option(key='yes',
                                value='Yes',
                                show_pane='pane_control_code'),
                         Option(key='no',
                                value='No'),
                         Option(key='unsure',
                                value='I don\'t know')
                     ],
                     classes=['govuk-radios--inline']),
        TextInput(title='What\'s your good\'s control list entry?',
                  description='<noscript>If your good is controlled, enter its control list entry. </noscript>For example, ML1a.',
                  name='control_code'),
        RadioButtons(title='Is your good intended to be incorporated into an end product?',
                     description='',
                     name='is_good_end_product',
                     options=[
                         Option(key=True,
                                value='Yes'),
                         Option(key=False,
                                value='No')
                     ],
                     classes=['govuk-radios--inline']),
        TextInput(title='Part Number',
                  name='part_number',
                  optional=True),
    ],
                buttons=[
                    Button('Save', 'submit', ButtonStyle.DEFAULT),
                    Button(value='Delete good',
                           action='',
                           style=ButtonStyle.WARNING,
                           link=reverse_lazy('goods:delete', kwargs={'pk': good_id}),
                           float_right=True),
                ])


def attach_documents_form(case_url):
    return Form(get_string('goods.documents.attach_documents.title'),
                get_string('goods.documents.attach_documents.description'),
                [
                    FileUpload('documents'),
                    TextArea(title=get_string('goods.documents.attach_documents.description_field_title'),
                             optional=True,
                             name='description',
                             extras={
                                 'max_length': 280,
                             })
                ],
                back_link=BackLink(get_string('goods.documents.attach_documents.back_to_good'), case_url))


def respond_to_query_form(good_id, ecju_query):
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
                back_link=BackLink('Back to good', reverse_lazy('goods:good_detail',
                                                                kwargs={'pk': good_id,
                                                                        'type': 'ecju-queries'})),
                default_button_name='Submit response')


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(title='Are you sure you want to send this response?',
                        confirmation_name='confirm_response',
                        hidden_field='ecju_query_response_confirmation',
                        yes_label='Yes, send the response',
                        no_label='No, change my response',
                        back_link_text='Back to edit response',
                        back_url=edit_response_url)


def delete_good_form(good):
    return Form(title='Are you sure you want to delete this good?',
                questions=[
                    good_summary(good)
                ],
                buttons=[
                    Button(value='Yes, delete the good', action='submit', style=ButtonStyle.WARNING),
                    Button(value='Cancel', action='', style=ButtonStyle.SECONDARY, link=reverse_lazy('goods:edit',
                                                                                                     kwargs={'pk': good['id']}))
                ])
