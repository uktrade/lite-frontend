from django.urls import reverse
from lite_forms.components import Form, Filter, Checkboxes, BackLink

from core.services import get_countries
from core.builtins.custom_tags import get_string


def countries_form(draft_id):
    return Form(title=get_string('licences.countries.title'),
                description=get_string('licences.countries.description'),
                questions=[
                    Filter(),
                    Checkboxes('countries', get_countries(None, True), classes=['govuk-checkboxes--small']),
                ],
                javascript_imports=['/assets/javascripts/filter-checkbox-list.js'],
                default_button_name='Save',
                back_link=BackLink(get_string('common.back_to_task_list'), reverse('applications:task_list',
                                                                                   kwargs={'pk': draft_id})))
