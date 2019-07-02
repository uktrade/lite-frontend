from libraries.forms.components import Form, Checkboxes, Filter
from sites.services import get_sites


def sites_form(request):
    return Form(title='Where are your goods located?',
                description='Select all sites that apply.',
                questions=[
                    Filter(),
                    Checkboxes('sites', get_sites(request, True))
                ],
                javascript_imports=['/assets/javascripts/filter-checkbox-list.js'],
                default_button_name='Save and continue')
