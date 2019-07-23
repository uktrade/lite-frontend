from core.services import get_countries
from libraries.forms.components import Form, Question, InputType, Section, ArrayQuestion, Option, RadioButtons


def new_end_user_form():
    return Section('', '', [
        Form(title='Who will be the final recipient (end-user) of your goods?',
             description='',
             questions=[
                 RadioButtons('type',
                              options=[
                                  Option('government', 'A Government Organisation'),
                                  Option('commercial', 'A Commercial Organisation'),
                                  Option('individual', 'An Individual'),
                                  Option('other', 'Other', show_or=True),
                              ]),
             ],
             pk='1',
             default_button_name='Continue'),
        Form(title='Enter the final recipient\'s name',
             description='',
             questions=[
                 Question('', '', InputType.INPUT, 'name'),
             ],
             pk='2',
             default_button_name='Continue'),
        Form(title='Enter the final recipient\'s web address (URL)',
             description='',
             questions=[
                 Question('', '', InputType.INPUT, 'website', optional=True),
             ],
             pk='3',
             default_button_name='Continue'),
        Form(title='Where\'s the final recipient based?',
             description='',
             questions=[
                 Question('Address', '', InputType.TEXTAREA, 'address'),
                 ArrayQuestion(title='Country',
                               description='',
                               input_type=InputType.AUTOCOMPLETE,
                               name='country',
                               data=get_countries(None, True)),
             ],
             pk='4',
             default_button_name='Save and continue')
    ])
