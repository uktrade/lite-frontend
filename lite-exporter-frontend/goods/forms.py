from conf.settings import env
from libraries.forms.components import Form, Question, ArrayQuestion, Option, InputType

form = Form(title='Add Good', description='', caption='', questions=[
    Question(title='Description of good',
             description='This can make it easier to find your good later',
             input_type=InputType.TEXTAREA,
             name='description',
             extras={
                 'max_length': 280,
             }),
    ArrayQuestion(title='Is your good controlled?',
                  description='If you don\'t know you can use <a class="govuk-link" href="' + env('PERMISSIONS_FINDER_URL') + '">Permissions Finder</a>.',
                  input_type=InputType.RADIOBUTTONS,
                  name='is_good_controlled',
                  data=[
                      Option(key='yes',
                             value='Yes',
                             show_pane='pane_control_code'),
                      Option(key='no',
                             value='No')
                  ]),
    Question(title='What\'s your good\'s control code?',
             description='<noscript>If your good is controlled, enter its control code. </noscript>For example, ML1a.',
             input_type=InputType.INPUT,
             name='control_code'),
    ArrayQuestion(title='Is your good intended to be incorporated into an end product?',
                  description='',
                  input_type=InputType.RADIOBUTTONS,
                  name='is_good_end_product',
                  data=[
                      Option(key='yes',
                             value='Yes'),
                      Option(key='no',
                             value='No')
                  ]),
    Question(title='Part Number',
             description='',
             input_type=InputType.INPUT,
             name='part_number',
             optional=True),
])
