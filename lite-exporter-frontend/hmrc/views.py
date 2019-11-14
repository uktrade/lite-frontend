from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.hmrc import confirm_organisation_form
from applications.services import post_applications
from conf.constants import HMRC_QUERY
from core.helpers import convert_dict_to_query_params
from core.permissions import validate_is_in_organisation_type
from core.services import get_organisations, get_organisation
from lite_forms.generators import form_page


class SelectAnOrganisation(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        validate_is_in_organisation_type(request, 'hmrc')
        return super(SelectAnOrganisation, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('search_term', '').strip()
        params = {'page': int(request.GET.get('page', 1))}

        if search_term:
            params['search_term'] = search_term

        organisations = get_organisations(request, org_type=['commercial', 'individual'], **params)
        params_str = convert_dict_to_query_params(params)

        context = {
            'organisations': organisations,
            'params': params,
            'page': params.pop('page'),
            'params_str': params_str,
            'show_error': kwargs.get('show_error', False)
        }
        return render(request, 'hmrc/select-organisation.html', context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        organisation = request.POST.get('organisation')

        if action == 'continue':
            if organisation:
                organisation = get_organisation(request, request.POST.get('organisation'))
                return form_page(request, confirm_organisation_form(organisation))
            else:
                # Return an error if the user hasn't selected an organisation
                return self.get(request, show_error=True, *args, **kwargs)
        else:
            # Create a draft HMRC application
            data = {
                'name': 'HMRC Query',
                'application_type': HMRC_QUERY,
                'organisation': organisation
            }

            response, _ = post_applications(request, data)

            return redirect(reverse_lazy('applications:task_list', kwargs={'pk': response['id']}))
