from core.builtins.custom_tags import get_string
from core.services import get_countries, get_external_locations
from libraries.forms.components import Form, ArrayQuestion, InputType, Option, Question

which_location_form = Form(title=get_string('goods.location_questions.location.title'),
                           description='You can only choose one type of location per application',
                           questions=[
                               ArrayQuestion('', '', InputType.RADIOBUTTONS, 'organisation_or_external', [
                                   Option('organisation', get_string('goods.location_questions.location.my_sites')),
                                   Option('external', get_string('goods.location_questions.location.external_locations')),
                               ])
                           ],
                           default_button_name='Continue')

def new_location_form():
    return Form(title='Add a new external location',
                description='',
                questions=[
                 Question('Company name', '', InputType.INPUT, 'name'),
                 Question('Address', '', InputType.TEXTAREA, 'address'),
                 ArrayQuestion(title='Country',
                               description='',
                               input_type=InputType.AUTOCOMPLETE,
                               name='country',
                               data=get_countries(None, True)),
                ],
                default_button_name='Save and continue')


def external_locations_form(request):
    return Form(title='Where are your goods located?',
                description='Select all external locations that apply.',
                questions=[
                    ArrayQuestion('', '', InputType.CHECKBOXES, 'external_locations', get_external_locations(request, True))
                ],
                default_button_name='Save and continue')
