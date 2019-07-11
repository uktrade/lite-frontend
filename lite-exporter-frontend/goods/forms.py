from conf.settings import env
from libraries.forms.components import Form, Question, ArrayQuestion, Option, InputType, Group, Section


add_goods_questions = Form(title='Add Good', description='', caption='', questions=[
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
                             value='No'),
                      Option(key='unsure',
                             value='I don\'t know',
                             show_pane='pane_not_sure_details')
                  ],
                  same_row=True),
    Question(title='What\'s your good\'s control code?',
             description='<noscript>If your good is controlled, enter its control code. </noscript>For example, ML1a.',
             input_type=InputType.INPUT,
             name='control_code'),
    Group('not_sure_details', [
        Question(
             title='What do you think is your good\'s control code?',
             description='<noscript>If your good is controlled, enter its control code. </noscript>For example, ML1a.',
             input_type=InputType.INPUT,
             optional=True,
             name='not_sure_details_control_code'),
        Question(
             title='Further details about your goods',
             description='Please enter details of why you don\'t know if your good is controlled',
             input_type=InputType.TEXTAREA,
             name='not_sure_details_details'),
    ]),
    ArrayQuestion(title='Is your good intended to be incorporated into an end product?',
                  description='',
                  input_type=InputType.RADIOBUTTONS,
                  name='is_good_end_product',
                  data=[
                      Option(key='yes',
                             value='Yes'),
                      Option(key='no',
                             value='No')
                  ],
                  same_row=True),
    Question(title='Part Number',
             description='',
             input_type=InputType.INPUT,
             name='part_number',
             optional=True),
])

are_you_sure = Form(title='Are you sure?',
                    description='By submitting you are creating a CLC query that cannot be altered',
                    questions=[
                        ArrayQuestion(title='CLC Confirmation',
                            input_type=InputType.RADIOBUTTONS,
                            name='clc_query_confirmation',
                            description='',
                            data=[
                                    Option(key='yes',
                                           value='Yes'),
                                    Option(key='no',
                                           value='No')
                                ],
                                same_row=True),
                            ]
                    )

edit_form = Form(title='Edit Good', description='', caption='', questions=[
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
                      Option(key=True,
                             value='Yes',
                             show_pane='pane_control_code'),
                      Option(key=False,
                             value='No')
                  ],
                  same_row=True),
    Question(title='What\'s your good\'s control code?',
             description='<noscript>If your good is controlled, enter its control code. </noscript>For example, ML1a.',
             input_type=InputType.INPUT,
             name='control_code'),
    ArrayQuestion(title='Is your good intended to be incorporated into an end product?',
                  description='',
                  input_type=InputType.RADIOBUTTONS,
                  name='is_good_end_product',
                  data=[
                      Option(key=True,
                             value='Yes'),
                      Option(key=False,
                             value='No')
                  ],
                  same_row=True),
    Question(title='Part Number',
             description='',
             input_type=InputType.INPUT,
             name='part_number',
             optional=True),
])
