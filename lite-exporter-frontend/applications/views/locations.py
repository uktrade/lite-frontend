from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.countries import countries_form
from applications.forms.locations import (
    which_location_form,
    new_location_form,
    external_locations_form,
    add_external_location,
    Locations,
    sites_form,
)
from applications.helpers.validators import validate_external_location_choice, validate_and_update_goods_location_choice
from applications.services import get_application, get_application_countries, post_application_countries
from core.services import (
    get_sites_on_draft,
    post_sites_on_draft,
    post_external_locations,
    get_external_locations_on_draft,
    post_external_locations_on_draft,
    delete_external_locations_from_draft,
)
from lite_forms.views import SingleFormView


class GoodsLocation(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        if not application["goods_locations"]:
            return redirect(reverse_lazy("applications:edit_location", kwargs={"pk": application_id}))

        return render(request, "applications/goods-locations/goods-locations.html", {"application": application})


class EditGoodsLocation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = which_location_form(self.object_pk, application.sub_type)
        self.action = validate_and_update_goods_location_choice
        self.data = {"choice": Locations.DEPARTED if application.get("have_goods_departed") else ""}

        if application.status == "submitted":
            if application["goods_locations"]:
                return reverse_lazy("applications:location", kwargs={"pk": self.object_pk})
            elif application["sites"]:
                return reverse_lazy("applications:existing_sites", kwargs={"pk": self.object_pk})

    def get_success_url(self):
        choice = self.get_validated_data()["choice"]
        if choice == Locations.EXTERNAL:
            return reverse_lazy("applications:select_add_external_location", kwargs={"pk": self.object_pk})
        elif choice == Locations.ORGANISATION:
            return reverse_lazy("applications:existing_sites", kwargs={"pk": self.object_pk})
        elif choice == Locations.DEPARTED:
            return reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})


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


class ExistingSites(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)

        if application.status == "submitted" and not application["goods_locations"]["type"] == "sites":
            raise Http404

        self.data, _ = get_sites_on_draft(request, self.object_pk)
        self.form = sites_form(request, application.type_reference)
        self.action = post_sites_on_draft
        self.success_url = reverse_lazy("applications:location", kwargs={"pk": self.object_pk})


class AddExternalLocation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = new_location_form(application.type_reference)
        self.action = post_external_locations
        self.success_url = reverse_lazy("applications:location", kwargs={"pk": self.object_pk})


class RemoveExternalLocation(TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        ext_loc_id = str(kwargs["ext_loc_pk"])
        delete_external_locations_from_draft(request, draft_id, ext_loc_id)

        return redirect(reverse_lazy("applications:location", kwargs={"pk": draft_id}))


class AddExistingExternalLocation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.data, _ = get_external_locations_on_draft(request, self.object_pk)
        self.form = external_locations_form(request, application.type_reference)
        self.action = post_external_locations_on_draft
        self.success_url = reverse_lazy("applications:location", kwargs={"pk": self.object_pk})


class Countries(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = {"countries": get_application_countries(request, self.object_pk)}
        self.form = countries_form(self.object_pk)
        self.action = post_application_countries
        self.success_url = reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})
