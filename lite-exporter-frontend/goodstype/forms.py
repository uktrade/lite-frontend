from lite_forms.components import TextArea, RadioButtons, Option, Form, TextInput

form = Form(title='Add a description', questions=[
    TextArea(title='Give a short description of your goods.',
             name='description',
             extras={
                 'max_length': 280,
             }),
    RadioButtons(title='Is your good controlled?',
                 description='If you don\'t know you can use <a class="govuk-link" target="_blank" '
                             'href="https://permissions-finder.service.trade.gov.uk/">Permissions Finder</a>.',
                 name='is_good_controlled',
                 options=[
                     Option(key='yes',
                            value='Yes',
                            show_pane='pane_control_code'),
                     Option(key='no',
                            value='No')
                 ],
                 classes=['govuk-radios--inline']),
    TextInput(title='What\'s your good\'s control list entry?',
              description='<noscript>If your good is controlled, enter its control list entry. </noscript>For example, ML1a.',
              name='control_code'),
    RadioButtons(title='Is your good intended to be incorporated into an end product?',
                 description='',
                 name='is_good_end_product',
                 options=[
                     Option(key='yes',
                            value='Yes'),
                     Option(key='no',
                            value='No')
                 ],
                 classes=['govuk-radios--inline'])
])
