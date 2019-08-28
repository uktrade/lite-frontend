from django.urls import reverse
from lite_forms.components import Form, Filter, Checkboxes, BackLink

from core.builtins.custom_tags import get_string
from core.services import get_countries


def countries_form(draft_id):
    return Form(title=get_string('licences.countries.title'),
                description=get_string('licences.countries.description'),
                questions=[
                    Filter(),
                    Checkboxes('countries', get_countries(None, True), classes=['govuk-checkboxes--small']),
                ],
                javascript_imports=['/assets/javascripts/filter-checkbox-list.js'],
                back_link=BackLink('Back to Overview', reverse('apply_for_a_licence:overview',
                                                               kwargs={'pk': draft_id})))
