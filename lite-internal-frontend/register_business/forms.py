from core.services import get_countries
from libraries.forms.components import Section, Form, Question, InputType, Button, HeadingStyle, Heading, \
    HelpSection, ArrayQuestion


def register_business_forms():
    return Section('', '', [
        Form(title='Register an organisation',
             description='Part 1 of 3',
             questions=[
                 Question(title='What\'s the organisation\'s name?',
                          description='',
                          input_type=InputType.INPUT,
                          name='name'),
                 Question(title='European Union registration and identification number (EORI)',
                          description='',
                          input_type=InputType.INPUT,
                          name='eori_number'),
                 Question(title='Standard Industrial Classification Number (SIC)',
                          description='Classifies industries by a four-digit code.',
                          input_type=InputType.INPUT,
                          name='sic_number'),
                 Question(title='UK VAT number',
                          description='9 digits long, with the first two letters indicating the'
                                      ' country code of the registered business.',
                          input_type=InputType.INPUT,
                          name='vat_number'),
                 Question(title='Company registration number (CRN)',
                          description='8 numbers, or 2 letters followed by 6 numbers.',
                          input_type=InputType.INPUT,
                          name='registration_number'),
             ],
             pk='1',
             buttons=[
                 Button('Save and continue', '')
             ],
             ),
        Form(title='Create a default site for this organisation',
             description='Part 2 of 3',
             questions=[
                 Question(title='Name of site',
                          description='',
                          input_type=InputType.INPUT,
                          name='site.name'),
                 Heading('Where is the organisation based?', HeadingStyle.M),
                 Question(title='Building and street',
                          description='<span class="govuk-visually-hidden">line 1 of 2</span>',
                          input_type=InputType.INPUT,
                          name='site.address.address_line_1'),
                 Question(title='',
                          description='<span class="govuk-visually-hidden">line 2 of 2</span>',
                          input_type=InputType.INPUT,
                          name='site.address.address_line_2'),
                 Question(title='Town or city',
                          description='',
                          input_type=InputType.INPUT,
                          name='site.address.city'),
                 Question(title='County/State',
                          description='',
                          input_type=InputType.INPUT,
                          name='site.address.region'),
                 Question(title='Postal Code',
                          description='',
                          input_type=InputType.INPUT,
                          name='site.address.postcode'),
                 ArrayQuestion(title='Country',
                               description='',
                               input_type=InputType.AUTOCOMPLETE,
                               name='site.address.country',
                               data=get_countries(None, True)),
             ],
             pk='2',
             buttons=[
                 Button('Save and continue', '')
             ]),
        Form('Create an admin for this organisation', 'Part 3 of 3', [
            Question(title='Email Address',
                     description='',
                     input_type=InputType.INPUT,
                     name='user.email'),
            Question(title='First name',
                     description='',
                     input_type=InputType.INPUT,
                     name='user.first_name'),
            Question(title='Last name',
                     description='',
                     input_type=InputType.INPUT,
                     name='user.last_name'),
        ],
             pk='3',
             buttons=[
                 Button('Submit', '')
             ], helpers=[
                HelpSection('Help', 'This will be the default user for this organisation.')
            ]),
    ])
