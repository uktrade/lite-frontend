from libraries.forms.components import Form, Question, Option, InputType, RadioButtons, TextArea

form = Form(title='Add a description', description='', caption='', questions=[
    TextArea(title='Give a short description of your goods.',
             description='',
             name='description',
             extras={
                 'max_length': 280,
             }),
    RadioButtons(title='Is your good controlled?',
                 description='If you don\'t know you can use <a class="govuk-link" target="_blank" href="https://permissions-finder.service.trade.gov.uk/">Permissions Finder</a>.',
                 name='is_good_controlled',
                 options=[
                     Option(key='yes',
                            value='Yes',
                            show_pane='pane_control_code'),
                     Option(key='no',
                            value='No')
                 ]),
    Question(title='What\'s your good\'s control list classification?',
             description='<noscript>If your good is controlled, enter its control list classification. </noscript>For example, ML1a.',
             input_type=InputType.INPUT,
             name='control_code'),
    RadioButtons(title='Is your good intended to be incorporated into an end product?',
                 description='',
                 name='is_good_end_product',
                 options=[
                     Option(key='yes',
                            value='Yes'),
                     Option(key='no',
                            value='No')
                 ])
])
