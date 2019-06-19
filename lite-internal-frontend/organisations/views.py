import requests

from django.shortcuts import render
from django.views.generic import TemplateView

from conf.settings import env
from organisations.services import get_organisations, get_organisations_sites, get_organisation_detail


class OrganisationList(TemplateView):

    def get(self, request, **kwargs):
        data, status_code = get_organisations(request)
        context = {
            'data': data,
            'title': 'Organisations',
        }
        return render(request, 'organisations/index.html', context)


class OrganisationDetail(TemplateView):

    def get(self, request, **kwargs):
        organisation, status_code = get_organisation(request, str(kwargs['pk']))
        sites, status_code = get_organisations_sites(request, str(kwargs['pk']))
        context = {
            'organisation': organisation['organisation'],
            'title': organisation['organisation']['name'],
            'sites': sites['sites'],
        }
        return render(request, 'organisations/organisation.html', context)
