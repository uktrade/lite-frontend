from django.urls import reverse
from lite_forms.components import Form, RadioButtons, Option, TextArea, Select, Filter, Checkboxes, TextInput, BackLink

from core.builtins.custom_tags import get_string
from core.services import get_countries, get_external_locations


def which_location_form(draft_id):
    return Form(title=get_string('goods.location_questions.location.title'),
                description='You can only choose one type of location per application',
                questions=[
                    RadioButtons('organisation_or_external', [
                        Option('organisation', get_string('goods.location_questions.location.my_sites')),
                        Option('external', get_string('goods.location_questions.location.external_locations')),
                    ])
                ],
                default_button_name='Continue',
                back_link=BackLink('Back to Overview', reverse('apply_for_a_licence:overview',
                                                               kwargs={'pk': draft_id})))


def new_location_form():
    return Form(title='Add a new external location',
                description='',
                questions=[
                    TextInput(title='Company name',
                              name='name'),
                    TextArea('address', 'Address'),
                    Select(title='Country',
                           description='',
                           name='country',
                           options=get_countries(None, True)),
                ],
                default_button_name='Save and continue')


def external_locations_form(request):
    return Form(title='Where are your goods located?',
                description='Select all external locations that apply.',
                questions=[
                    Filter(),
                    Checkboxes('external_locations', get_external_locations(request, str(request.user.organisation), True))
                ],
                javascript_imports=['/assets/javascripts/filter-checkbox-list.js'],
                default_button_name='Save and continue')
