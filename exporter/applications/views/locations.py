from operator import itemgetter

from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, FormView
from django.utils.functional import cached_property

from exporter.applications.forms.countries import (
    countries_form,
    choose_contract_type_form,
    contract_type_per_country_form,
)
from exporter.applications.forms.locations import (
    which_location_form,
    external_locations_form,
    add_external_location,
    Locations,
    sites_form,
    new_external_location_form,
)
from exporter.applications.forms import locations as location_forms
from exporter.applications.helpers.check_your_answers import is_application_oiel_of_type
from exporter.applications.helpers.countries import prettify_country_data
from exporter.applications.helpers.task_list_sections import get_product_location_and_journey_details
from exporter.applications.helpers.validators import (
    validate_external_location_choice,
    validate_and_update_goods_location_choice,
    validate_contract_type_countries_choice,
)
from exporter.applications.services import (
    get_application,
    get_application_countries,
    post_application_countries,
    put_application_simple,
    put_contract_type_for_country,
    get_application_countries_and_contract_types,
)
from exporter.core.constants import CaseTypes, APPLICANT_EDITING
from exporter.core.services import (
    get_sites_on_draft,
    post_sites_on_draft,
    post_external_locations,
    get_external_locations_on_draft,
    post_external_locations_on_draft,
    delete_external_locations_from_draft,
)
from lite_content.lite_exporter_frontend.applications import ContractTypes
from lite_forms.views import SingleFormView, MultiFormView

from core.auth.views import LoginRequiredMixin


class ApplicationMixin:
    @cached_property
    def application(self):
        return get_application(self.request, self.kwargs["pk"])


def get_locations_page(request, application_id, **kwargs):
    application = get_application(request, application_id)

    if not application["goods_locations"]:
        return redirect(reverse_lazy("applications:edit_location", kwargs={"pk": application_id}))

    context = {
        "application": application,
        "is_application_draft_or_major_edit": application["status"]["key"] in [APPLICANT_EDITING, "draft"],
    }

    if kwargs.get("errors"):
        context["errors"] = kwargs["errors"]

    return render(
        request,
        "applications/goods-locations/goods-locations.html",
        context,
    )


class GoodsLocation(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        return get_locations_page(request, application_id=kwargs["pk"])


class GoodsLocationView(LoginRequiredMixin, ApplicationMixin, TemplateView):
    template_name = "applications/goods-locations/goods-locations.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["application"] = self.application
        context["is_application_draft_or_major_edit"] = self.application["status"]["key"] in [
            APPLICANT_EDITING,
            "draft",
        ]
        return context

    def dispatch(self, *args, **kwargs):
        has_old_locations = self.application["goods_locations"]
        has_new_locations = (
            self.application.get("goods_recipients", False)
            and self.application.get("goods_starting_point", False)
            and self.application["export_type"]
            and self.application["is_shipped_waybill_or_lading"]
        )
        task_list_url = reverse("applications:task_list", kwargs={"pk": self.kwargs["pk"]})
        if has_old_locations:
            return super().dispatch(*args, **kwargs)
        elif not has_old_locations and not has_new_locations:
            return redirect(reverse("applications:edit_location", kwargs={"pk": self.kwargs["pk"]}))
        elif has_new_locations:
            summary_url = reverse("applications:locations_summary", kwargs={"pk": self.kwargs["pk"]})
            return redirect(f"{summary_url}?return_to={task_list_url}")


class GoodsStartingPointFormView(LoginRequiredMixin, ApplicationMixin, FormView):
    template_name = "core/form.html"
    form_class = location_forms.GoodsStartingPointForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["back_link_url"] = reverse("applications:task_list", kwargs={"pk": self.kwargs["pk"]})
        return context

    def get_initial(self):
        return {"goods_starting_point": self.application["goods_starting_point"]}

    def get_success_url(self):
        return reverse("applications:export_details", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        put_application_simple(self.request, self.kwargs["pk"], form.cleaned_data)
        return super().form_valid(form)


class TemporaryOrPermanentFormView(LoginRequiredMixin, ApplicationMixin, FormView):
    template_name = "core/form.html"
    form_class = location_forms.PermanentOrTemporaryExportForm

    def get_initial(self):
        if self.application["export_type"]:
            return {"export_type": self.application["export_type"]["key"]}
        return {}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["back_link_url"] = reverse("applications:edit_location", kwargs={"pk": self.kwargs["pk"]})
        return context

    def form_valid(self, form):
        put_application_simple(self.request, self.kwargs["pk"], form.cleaned_data)
        if form.cleaned_data["export_type"] == "temporary":
            return redirect(reverse("applications:export_details", kwargs={"pk": self.kwargs["pk"]}))
        else:
            return redirect(reverse("applications:route_of_goods", kwargs={"pk": self.kwargs["pk"]}))


class GoodsRecipientsFormView(LoginRequiredMixin, ApplicationMixin, FormView):
    template_name = "core/form.html"
    form_class = location_forms.GoodsRecipientsForm

    def get_initial(self):
        return {
            "goods_recipients": self.application.get("goods_recipients", False),
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["back_link_url"] = reverse("applications:route_of_goods", kwargs={"pk": self.kwargs["pk"]})
        return context

    def form_valid(self, form):
        put_application_simple(self.request, self.kwargs["pk"], form.cleaned_data)
        return redirect(reverse("applications:locations_summary", kwargs={"pk": self.kwargs["pk"]}))


class LocationsSummaryView(LoginRequiredMixin, ApplicationMixin, TemplateView):
    template_name = "applications/goods-locations/goods-locations-summary.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["application"] = self.application

        has_product_journey = get_product_location_and_journey_details(self.application)
        if has_product_journey:
            back_link_url = reverse("applications:task_list", kwargs={"pk": self.kwargs["pk"]})
        else:
            back_link_url = reverse("applications:export_details", kwargs={"pk": self.kwargs["pk"]})

        context["back_link_url"] = back_link_url
        return context


class EditGoodsLocation(LoginRequiredMixin, SingleFormView):
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
            return (
                reverse_lazy("applications:select_add_external_location", kwargs={"pk": self.object_pk})
                + "?return_to="
                + self.request.get_full_path()
            )
        elif choice == Locations.ORGANISATION:
            return reverse_lazy("applications:existing_sites", kwargs={"pk": self.object_pk})
        elif choice == Locations.DEPARTED:
            return reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})


class SelectAddExternalLocation(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = add_external_location(request)
        self.action = validate_external_location_choice

    def get_success_url(self):
        choice = self.get_validated_data()["choice"]
        if choice == "new":
            return (
                reverse_lazy("applications:add_external_location", kwargs={"pk": self.object_pk})
                + "?return_to="
                + self.request.get_full_path()
            )
        else:
            return reverse_lazy("applications:add_preexisting_external_location", kwargs={"pk": self.object_pk})


class ExistingSites(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)

        if application.status == "submitted" and not application["goods_locations"]["type"] == "sites":
            raise Http404

        self.data, _ = get_sites_on_draft(request, self.object_pk)
        self.form = sites_form(request, application.type_reference)
        self.action = post_sites_on_draft
        self.success_url = reverse_lazy("applications:location", kwargs={"pk": self.object_pk})


class AddExternalLocation(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        location_type = request.POST.get("location_type", None)
        self.forms = new_external_location_form(request, application.type_reference, location_type)
        self.action = post_external_locations
        self.success_url = reverse_lazy("applications:location", kwargs={"pk": self.object_pk})


class RemoveExternalLocation(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        draft_id = str(kwargs["pk"])
        ext_loc_id = str(kwargs["ext_loc_pk"])
        data, _ = delete_external_locations_from_draft(request, draft_id, ext_loc_id)

        parameters = {
            "request": request,
            "application_id": draft_id,
        }

        if data.get("errors"):
            parameters["errors"] = data["errors"]["external_locations"]

        return get_locations_page(**parameters)


class AddExistingExternalLocation(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.data, _ = get_external_locations_on_draft(request, self.object_pk)
        self.form = external_locations_form(request, application.type_reference)
        self.action = post_external_locations_on_draft
        self.success_url = reverse_lazy("applications:location", kwargs={"pk": self.object_pk})


class Countries(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.data = {
            "countries": [
                country_entry["country_id"]
                for country_entry in get_application_countries_and_contract_types(request, self.object_pk)["countries"]
            ]
        }
        self.form = countries_form(request, self.object_pk)
        self.action = post_application_countries

    def get_success_url(self):
        application = get_application(self.request, self.object_pk)

        # Only military OIELs and Open Trade Control Licences have contract types per destination
        if not (is_application_oiel_of_type("military", application) or application.type_reference == CaseTypes.OICL):
            return reverse_lazy("applications:task_list", kwargs={"pk": self.object_pk})

        countries_without_contract_type = [
            entry["country_id"]
            for entry in get_application_countries_and_contract_types(self.request, self.object_pk)["countries"]
            if not entry["contract_types"]
        ]

        if not countries_without_contract_type:
            return reverse_lazy("applications:countries_summary", kwargs={"pk": self.object_pk})
        else:
            return reverse_lazy("applications:choose_contract_type", kwargs={"pk": self.object_pk})


class ChooseContractType(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.form = choose_contract_type_form()
        self.action = validate_contract_type_countries_choice

    def get_success_url(self):
        choice = self.get_validated_data()["choice"]
        countries_without_contract_type = [
            entry["country_id"]
            for entry in get_application_countries_and_contract_types(self.request, self.object_pk)["countries"]
            if not entry["contract_types"]
        ]

        if choice == ContractTypes.Variables.ALL_COUNTRIES_CHOSEN:
            return reverse_lazy(
                "applications:add_contract_type",
                kwargs={"pk": self.object_pk, "country": ContractTypes.Variables.ALL_COUNTRIES_CHOSEN},
            )
        if countries_without_contract_type:
            return reverse_lazy(
                "applications:add_contract_type",
                kwargs={"pk": self.object_pk, "country": countries_without_contract_type[0]},
            )
        else:
            # Redirect to the summary page if a country has been removed
            return reverse_lazy("applications:countries_summary", kwargs={"pk": self.object_pk})


class AddContractTypes(LoginRequiredMixin, SingleFormView):
    contract_types_and_countries = None

    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.action = put_contract_type_for_country
        self.contract_types_and_countries = get_application_countries_and_contract_types(request, self.object_pk)[
            "countries"
        ]
        current_country = self.kwargs["country"]
        selected_countries = [country_entry["country_id"] for country_entry in self.contract_types_and_countries]
        data_for_current_country = [
            country_entry
            for country_entry in self.contract_types_and_countries
            if country_entry["country_id"] == current_country
        ]
        self.data = (
            {
                "contract_types": data_for_current_country[0]["contract_types"].split(",")
                if data_for_current_country[0]["contract_types"]
                else None,
                "other_contract_type_text": data_for_current_country[0]["other_contract_type_text"],
            }
            if data_for_current_country
            else {}
        )

        if current_country != ContractTypes.Variables.ALL_COUNTRIES_CHOSEN:
            if current_country == "UKCS":
                country_name = "UK Continental Shelf"
            else:
                country_name = data_for_current_country[0]["country__name"]
            if country_name not in str(self.contract_types_and_countries):
                return render(request, "404.html")
            self.form = contract_type_per_country_form([current_country], country_name)
        else:
            selected_countries_ids = selected_countries
            self.form = contract_type_per_country_form(selected_countries_ids, "all the countries")

    def get_success_url(self):
        # Go through all countries without contract types and render the form again if needed
        next_country = None
        if self.kwargs["country"] != ContractTypes.Variables.ALL_COUNTRIES_CHOSEN:
            for country_entry in self.contract_types_and_countries:
                # If a country has no contract types and it is not the current country (still empty as we do not do an additional call to the api)
                if not country_entry["contract_types"] and country_entry["country_id"] != self.kwargs["country"]:
                    next_country = country_entry["country_id"]
                    break
        if next_country:
            return reverse_lazy(
                "applications:add_contract_type", kwargs={"pk": self.object_pk, "country": next_country}
            )
        else:
            return reverse_lazy("applications:countries_summary", kwargs={"pk": self.object_pk})


class CountriesAndContractTypesSummary(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        object_pk = kwargs["pk"]
        countries_data = get_application_countries_and_contract_types(request, object_pk)
        countries = [
            {
                "country_id": country_entry["country_id"],
                "country_name": country_entry["country__name"],
                "contract_types": country_entry["contract_types"],
                "other_contract_type_text": country_entry["other_contract_type_text"],
            }
            for country_entry in countries_data["countries"]
        ]

        prettified_countries = prettify_country_data(sorted(countries, key=itemgetter("country_name")))
        context = {
            "application_id": str(object_pk),
            "is_application_oiel_continental_shelf": len(countries) == 1 and countries[0]["country_id"] == "UKCS",
            "countries": prettified_countries,
            "is_application_draft_or_major_edit": countries_data["status"] in [APPLICANT_EDITING, "draft"],
        }

        return render(request, "applications/goods-locations/destinations-summary-list.html", context)


class StaticDestinations(LoginRequiredMixin, TemplateView):
    # To be used for OIELs where all countries are preselected and non-modifiable by the user
    # The UKCS OIEL is a special case - this is the initial page displayed before prompting the user to select contract types
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        goodstype_category = None

        if application.get("goodstype_category"):
            goodstype_category = application.get("goodstype_category").get("key")
            goodstype_category_label = application.get("goodstype_category").get("value")

        context = {
            "application_id": application_id,
            "countries": get_application_countries(request, application_id),
            "goodstype_category": goodstype_category,
            "goodstype_category_label": goodstype_category_label,
        }

        return render(request, "applications/goods-locations/static-all-destinations.html", context)
