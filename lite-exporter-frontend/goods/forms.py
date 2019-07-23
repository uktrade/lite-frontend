from conf.settings import env
from libraries.forms.components import Form, Question, Option, InputType, Group, RadioButtons

add_goods_questions = Form(title='Add Good', description='', caption='', questions=[
    Question(title='Description of good',
             description='This can make it easier to find your good later',
             input_type=InputType.TEXTAREA,
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
                            value='I don\'t know',
                            show_pane='pane_not_sure_details')
                 ],
                 classes=['govuk-radios--inline']),
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
    RadioButtons(title='Is your good intended to be incorporated into an end product?',
                 description='',
                 name='is_good_end_product',
                 options=[
                     Option(key='yes',
                            value='Yes'),
                     Option(key='no',
                            value='No')
                 ],
                 classes=['govuk-radios--inline']),
    Question(title='Part Number',
             description='',
             input_type=InputType.INPUT,
             name='part_number',
             optional=True),
])

are_you_sure = Form(title='Are you sure?',
                    description='By submitting you are creating a CLC query that cannot be altered',
                    questions=[
                        RadioButtons(title='CLC Confirmation',
                                     name='clc_query_confirmation',
                                     description='',
                                     options=[
                                         Option(key='yes',
                                                value='Yes'),
                                         Option(key='no',
                                                value='No')
                                     ],
                                     classes=['govuk-radios--inline']),
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
    RadioButtons(title='Is your good controlled?',
                 description='If you don\'t know you can use <a class="govuk-link" href="' + env(
                     'PERMISSIONS_FINDER_URL') + '">Permissions Finder</a>.',
                 name='is_good_controlled',
                 options=[
                     Option(key='yes',
                            value='Yes',
                            show_pane='pane_control_code'),
                     Option(key='no',
                            value='No')
                 ],
                 classes=['govuk-radios--inline']),
    Question(title='What\'s your good\'s control code?',
             description='<noscript>If your good is controlled, enter its control code. </noscript>For example, ML1a.',
             input_type=InputType.INPUT,
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
    Question(title='Part Number',
             description='',
             input_type=InputType.INPUT,
             name='part_number',
             optional=True),
])
