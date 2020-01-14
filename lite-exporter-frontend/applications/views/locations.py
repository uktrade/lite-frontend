from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.countries import countries_form
from applications.forms.location import (
    which_location_form,
    new_location_form,
    external_locations_form,
    add_external_location,
)
from applications.forms.sites import sites_form
from applications.services import get_application, get_application_countries, post_application_countries
from applications.helpers.validators import validate_external_location_choice
from core.services import (
    get_sites_on_draft,
    post_sites_on_draft,
    post_external_locations,
    get_external_locations_on_draft,
    post_external_locations_on_draft,
    delete_external_locations_from_draft,
)
from lite_forms.generators import form_page
from lite_forms.submitters import submit_single_form
from lite_forms.views import SingleFormView


class GoodsLocation(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if not application["goods_locations"]:
            return redirect(reverse_lazy("applications:edit_location", kwargs={"pk": application_id}))

        return render(request, "applications/goods-locations/goods-locations.html", {"application": application})


class EditGoodsLocation(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if application["goods_locations"]:
            if application["status"] and application["status"].get("key") == "submitted":
                return redirect(reverse_lazy("applications:location", kwargs={"pk": application_id}))
        else:
            if application["status"] and application["status"].get("key") == "submitted":
                return redirect(reverse_lazy("applications:existing_sites", kwargs={"pk": application_id}))

        return form_page(request, which_location_form(application_id))

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        data = request.POST.copy()

        if "organisation_or_external" not in data:
            errors = {"organisation_or_external": ["Select where the products are located"]}

            return form_page(request, which_location_form(draft_id), errors=errors)

        if data["organisation_or_external"] == "external":
            return redirect(reverse_lazy("applications:select_add_external_location", kwargs={"pk": draft_id}))
        else:
            return redirect(reverse_lazy("applications:existing_sites", kwargs={"pk": draft_id}))


class SelectAddExternalLocation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = add_external_location()
        self.action = validate_external_location_choice

    def get_success_url(self):
        choice = self.get_validated_data()["choice"]
        if choice == "new":
            return reverse_lazy("applications:add_external_location", kwargs={"pk": self.object_pk})
        else:
            return reverse_lazy("applications:add_preexisting_external_location", kwargs={"pk": self.object_pk})


class ExistingSites(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        response, _ = get_sites_on_draft(request, application_id)

        if application["status"] and application["status"].get("key") == "submitted" and not response["sites"]:
            raise Http404

        return form_page(request, sites_form(request), data=response)

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        data = {"sites": request.POST.getlist("sites")}

        response, status_code = post_sites_on_draft(request, draft_id, data)

        if status_code != 201:
            return form_page(request, sites_form(request), errors=response.get("errors"), data=data)

        return redirect(reverse_lazy("applications:location", kwargs={"pk": draft_id}))


# External Locations


class AddExternalLocation(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        response, _ = get_sites_on_draft(request, draft_id)

        return form_page(request, new_location_form(), data=response)

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        response, response_data = submit_single_form(
            request, new_location_form(), post_external_locations, object_pk=str(request.user.organisation)
        )

        if response:
            return response
        id = response_data["external_location"]["id"]

        # Append the new external location to the list of external locations rather than clearing them
        data = {"external_locations": [id], "method": "append_location"}
        data, status_code = post_external_locations_on_draft(request, draft_id, data)

        if status_code == 400:
            return form_page(request, new_location_form(), data=request.POST, errors=data["errors"])

        # If there is no response (no forms left to go through), go to the overview page
        return redirect(reverse_lazy("applications:location", kwargs={"pk": draft_id}))


class RemoveExternalLocation(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        ext_loc_id = str(kwargs["ext_loc_pk"])
        delete_external_locations_from_draft(request, draft_id, ext_loc_id)

        return redirect(reverse_lazy("applications:location", kwargs={"pk": draft_id}))


class AddExistingExternalLocation(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        data, _ = get_external_locations_on_draft(request, draft_id)

        return form_page(request, external_locations_form(request), data=data)

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])

        data = {"external_locations": request.POST.getlist("external_locations")}

        response, status_code = post_external_locations_on_draft(request, draft_id, data)

        if status_code != 201:
            return form_page(request, external_locations_form(request), errors=response.get("errors"))

        return redirect(reverse_lazy("applications:location", kwargs={"pk": draft_id}))


# Countries


class Countries(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        countries = {"countries": get_application_countries(request, draft_id)}

        return form_page(request, countries_form(draft_id), data=countries)

    def post(self, request, **kwargs):
        draft_id = str(kwargs["pk"])

        data = {"countries": request.POST.getlist("countries")}

        response, _ = submit_single_form(
            request, countries_form(draft_id), post_application_countries, object_pk=draft_id, override_data=data
        )

        if response:
            return response

        return redirect(reverse_lazy("applications:task_list", kwargs={"pk": draft_id}))
