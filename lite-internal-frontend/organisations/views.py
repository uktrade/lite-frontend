from django.shortcuts import render
from django.views.generic import TemplateView

from organisations.services import get_organisations, get_organisations_sites, get_organisation


class OrganisationList(TemplateView):
    """
    Show all organisations.
    """
    def get(self, request, **kwargs):
        data, _ = get_organisations(request)
        context = {
            'data': data,
            'title': 'Organisations',
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
            'organisation': data['organisation'],
            'title': data['organisation']['name'],
            'sites': sites['sites'],
        }
        return render(request, 'organisations/organisation.html', context)
