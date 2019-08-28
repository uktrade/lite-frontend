from lite_forms.components import RadioButtons, Form, Option, TextArea, Select, TextInput, FormGroup

from core.services import get_countries


def new_end_user_forms():
    return FormGroup([
        Form(title='Who will be the final recipient (end-user) of your goods?',
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
        Form(title='Enter the final recipient\'s name',
             questions=[
                 TextInput('name'),
             ],
             default_button_name='Continue'),
        Form(title='Enter the final recipient\'s web address (URL)',
             questions=[
                 TextInput('website', optional=True),
             ],
             default_button_name='Continue'),
        Form(title='Where\'s the final recipient based?',
             questions=[
                 TextArea('address', 'Address'),
                 Select(title='Country',
                        name='country',
                        options=get_countries(None, True)),
             ],
             default_button_name='Save and continue')
    ])
