from django.urls import reverse
from lite_forms.components import Form, TextArea, RadioButtons, Option, BackLink, FileUpload, TextInput

from conf.settings import env
from core.builtins.custom_tags import get_string

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
    TextInput(title='What\'s your good\'s control rating?',
              description='<noscript>If your good is controlled, enter its control rating. </noscript>For example, ML1a.',
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
                        title='What do you think is your good\'s control rating?',
                        description='<noscript>If your good is controlled, enter its control rating. </noscript>For example, ML1a.',
                        optional=True,
                        name='not_sure_details_control_code'),
                    TextArea(
                        title='Further details about your goods',
                        description='Please enter details of why you don\'t know if your good is controlled',
                        name='not_sure_details_details'),
                ],
                back_link=BackLink('Back to good', reverse('goods:good',
                                                           kwargs={'pk': good_id}))
                )


edit_form = Form(title='Edit Good', questions=[
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
    TextInput(title='What\'s your good\'s control rating?',
              description='<noscript>If your good is controlled, enter its control rating. </noscript>For example, ML1a.',
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
