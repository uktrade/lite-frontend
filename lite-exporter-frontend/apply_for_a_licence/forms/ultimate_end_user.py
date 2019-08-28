from lite_forms.components import Form, RadioButtons, Option, TextArea, Select, TextInput, FormGroup

from core.services import get_countries


def new_ultimate_end_user_form():
    return FormGroup([
        Form(title='How would you describe this recipient of your goods?',
             questions=[
                 RadioButtons('type',
                              options=[
                                  Option('government', 'A Government Organisation'),
                                  Option('commercial', 'A Commercial Organisation'),
                                  Option('individual', 'An Individual'),
                                  Option('other', 'Other', show_or=True),
                              ]),
             ],
             default_button_name='Continue'),
        Form(title='Enter the recipient\'s name',
             questions=[
                 TextInput('name'),
             ],
             default_button_name='Continue'),
        Form(title='Enter the recipient\'s web address (URL)',
             questions=[
                 TextInput('website', optional=True),
             ],
             default_button_name='Continue'),
        Form(title='Where\'s the recipient based?',
             questions=[
                 TextArea('address', 'Address'),
                 Select(title='Country',
                        description='',
                        name='country',
                        options=get_countries(None, True)),
             ],
             default_button_name='Save and continue')
    ])
