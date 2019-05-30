from libraries.forms.components import Form, ArrayQuestion, InputType
from sites.services import get_sites


def sites_form(request):
    return Form(title='Where are your goods located?',
                description='Select all sites that apply.',
                questions=[
                    ArrayQuestion('', '', InputType.CHECKBOXES, 'sites', get_sites(request, True))
                ],
                default_button_name='Save and continue')
