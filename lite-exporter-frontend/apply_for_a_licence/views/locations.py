from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form

from apply_for_a_licence.forms.countries import countries_form
from apply_for_a_licence.forms.location import which_location_form, new_location_form, external_locations_form
from apply_for_a_licence.forms.sites import sites_form
from core.services import get_sites_on_draft, post_sites_on_draft, post_external_locations, \
    get_external_locations_on_draft, get_external_locations, post_external_locations_on_draft
from drafts.services import get_draft, get_draft_countries, post_draft_countries


class Location(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = get_external_locations_on_draft(request, draft_id)
        if data['external_locations']:
            data = {'organisation_or_external': 'external'}
        else:
            data = {'organisation_or_external': 'organisation'}

        return form_page(request, which_location_form(draft_id), data=data)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])

        data = request.POST.copy()

        if 'organisation_or_external' not in data:
            errors = {
                'organisation_or_external': ['Select which one you want']
            }

            return form_page(request, which_location_form(draft_id), errors=errors)

        if data['organisation_or_external'] == 'external':
            return redirect(reverse_lazy('apply_for_a_licence:external_locations', kwargs={'pk': draft_id}))
        else:
            return redirect(reverse_lazy('apply_for_a_licence:existing_sites', kwargs={'pk': draft_id}))


# Existing Sites


class ExistingSites(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        response, status_code = get_sites_on_draft(request, draft_id)

        return form_page(request, sites_form(request), data=response)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)

        data = {
            'sites': request.POST.getlist('sites')
        }

        response, status_code = post_sites_on_draft(request, draft_id, data)

        if status_code != 201:
            return form_page(request, sites_form(request), errors=response.get('errors'))

        return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': draft_id}))


# External Locations


class ExternalLocations(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        draft, status_code = get_draft(request, draft_id)
        org_external_locations, status_code = get_external_locations(request, request.user.organisation)
        data, status_code = get_external_locations_on_draft(request, draft_id)

        context = {
            'title': 'External Locations',
            'org_external_locations': org_external_locations,
            'draft_id': draft_id,
            'data': data,
            'draft': draft,
        }
        return render(request, 'apply_for_a_licence/external_locations/index.html', context)


class AddExternalLocation(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        response, status_code = get_sites_on_draft(request, draft_id)

        return form_page(request, new_location_form(), data=response)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        response, response_data = submit_single_form(request, new_location_form(), post_external_locations,
                                                     pk=str(request.user.organisation))

        # If there are more forms to go through, continue
        if response:
            return response
        id = response_data['external_location']['id']

        # Append the new external location to the list of external locations rather than clearing them
        data = {
            'external_locations': [id],
            'method': 'append_location'
        }
        post_external_locations_on_draft(request, draft_id, data)

        # If there is no response (no forms left to go through), go to the overview page
        return redirect(reverse_lazy('apply_for_a_licence:external_locations', kwargs={'pk': draft_id}))


class AddExistingExternalLocation(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        data, status_code = get_external_locations_on_draft(request, draft_id)

        return form_page(request, external_locations_form(request), data=data)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])

        data = {
            'external_locations': request.POST.getlist('external_locations')
        }

        response, status_code = post_external_locations_on_draft(request, draft_id, data)

        if status_code != 201:
            return form_page(request, external_locations_form(request), errors=response.get('errors'))

        return redirect(reverse_lazy('apply_for_a_licence:external_locations', kwargs={'pk': draft_id}))


# Countries


class Countries(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs['pk'])
        countries, status_code = get_draft_countries(request, draft_id)

        return form_page(request, countries_form(draft_id), data=countries)

    def post(self, request, **kwargs):
        draft_id = str(kwargs['pk'])

        data = {
            'countries': request.POST.getlist('countries')
        }

        response, response_data = submit_single_form(request, countries_form(draft_id), post_draft_countries,
                                                     pk=draft_id, override_data=data)

        if response:
            return response

        return redirect(reverse_lazy('apply_for_a_licence:overview', kwargs={'pk': draft_id}))
