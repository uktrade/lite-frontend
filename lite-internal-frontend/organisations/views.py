from django.shortcuts import render
from django.views.generic import TemplateView

from core.helpers import convert_dict_to_query_params
from organisations.services import get_organisations, get_organisations_sites, get_organisation


class OrganisationList(TemplateView):
    """
    Show all organisations.
    """
    def get(self, request, **kwargs):
        name = request.GET.get('name', '').strip()
        org_type = request.GET.get('org_type', '').strip()

        params = {'page': int(request.GET.get('page', 1))}
        if name:
            params['name'] = name
        if org_type:
            params['org_type'] = org_type

        organisations, _ = get_organisations(request, convert_dict_to_query_params(params))

        context = {
            'data': organisations,
            'title': 'Organisations',
            'page': params.pop('page'),
            'params': params,
            'params_str': convert_dict_to_query_params(params)
        }
        return render(request, 'organisations/index.html', context)


class OrganisationDetail(TemplateView):
    """
    Show an organisation.
    """
    def get(self, request, **kwargs):
        organisation_pk = str(kwargs['pk'])
        data, _ = get_organisation(request, organisation_pk)
        sites, _ = get_organisations_sites(request, organisation_pk)

        context = {
            'organisation': data,
            'title': data['name'],
            'sites': sites['sites'],
        }
        return render(request, 'organisations/organisation.html', context)


class HMRCList(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_organisations(request, convert_dict_to_query_params({'org_type': 'hmrc'}))
        context = {
            'data': data,
            'title': 'Organisations',
        }
        return render(request, 'organisations/hmrc/index.html', context)
