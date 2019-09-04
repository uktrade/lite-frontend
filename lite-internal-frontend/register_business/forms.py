from lite_forms.common import address_questions
from lite_forms.components import Form, TextInput, Heading, HelpSection, FormGroup
from lite_forms.styles import HeadingStyle

from core.services import get_countries


def register_business_forms():
    return FormGroup([
        Form(title='Register an organisation',
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
             default_button_name='Continue'
             ),
        Form(title='Create a default site for this organisation',
             questions=[
                 TextInput(title='Name of site',
                           name='site.name'),
                 Heading('Where is the organisation based?', HeadingStyle.M),
                 *address_questions(get_countries(None, True), 'site.address.'),
             ],
             default_button_name='Continue'),
        Form(title='Create an admin for this organisation',
             questions=[
                 TextInput(title='Email Address',
                           name='user.email'),
                 TextInput(title='First name',
                           name='user.first_name'),
                 TextInput(title='Last name',
                           name='user.last_name'),
             ],
             default_button_name='Submit',
             helpers=[
                 HelpSection('Help', 'This will be the default user for this organisation.')
             ]),
    ],
        show_progress_indicators=True,)
