from lite_forms.common import address_questions
from lite_forms.components import Form, TextInput, Button, Heading, HelpSection, FormGroup
from lite_forms.styles import HeadingStyle

from core.services import get_countries


def register_business_forms():
    return FormGroup([
        Form(title='Register an organisation',
             description='Part 1 of 3',
             questions=[
                 TextInput(title='What\'s the organisation\'s name?',
                           name='name'),
                 TextInput(title='European Union registration and identification number (EORI)',
                           name='eori_number'),
                 TextInput(title='Standard Industrial Classification Number (SIC)',
                           description='Classifies industries by a four-digit code.',
                           name='sic_number'),
                 TextInput(title='UK VAT number',
                           description='9 digits long, with the first two letters indicating the'
                                       ' country code of the registered business.',
                           name='vat_number'),
                 TextInput(title='Company registration number (CRN)',
                           description='8 numbers, or 2 letters followed by 6 numbers.',
                           name='registration_number'),
             ],
             buttons=[
                 Button('Save and continue', '')
             ],
             ),
        Form(title='Create a default site for this organisation',
             description='Part 2 of 3',
             questions=[
                 TextInput(title='Name of site',
                           name='site.name'),
                 Heading('Where is the organisation based?', HeadingStyle.M),
                 *address_questions(get_countries(None, True), 'site.address.'),
             ],
             buttons=[
                 Button('Save and continue', '')
             ]),
        Form('Create an admin for this organisation', 'Part 3 of 3', [
            TextInput(title='Email Address',
                      name='user.email'),
            TextInput(title='First name',
                      name='user.first_name'),
            TextInput(title='Last name',
                      name='user.last_name'),
        ],
             buttons=[
                 Button('Submit', '')
             ], helpers=[
                HelpSection('Help', 'This will be the default user for this organisation.')
            ]),
    ])
