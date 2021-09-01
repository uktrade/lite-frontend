from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import redirect

from formtools.wizard.views import SessionWizardView

from exporter.core.services import get_organisation
from lite_forms.views import SingleFormView
from exporter.organisation.sites.forms import edit_site_name_form, site_records_location
from exporter.organisation.sites.services import get_site, post_sites, update_site, get_sites
from exporter.organisation.views import OrganisationView
from exporter.organisation.sites import forms as site_forms
from exporter.core.helpers import str_to_bool

from core.auth.views import LoginRequiredMixin


LOCATION = "location"
UK_ADDRESS = "uk_address"
INTERNATIONAL_ADDRESS = "international_address"
CONFIRM = "confirm"
ASSIGN_USERS = "assign_users"


class Sites(OrganisationView):
    template_name = "sites/index"

    def get_additional_context(self):
        return {"sites": get_sites(self.request, self.organisation_id, get_total_users=True)}


def show_international_site_form(wizard):
    # try to get the cleaned data of location step
    cleaned_data = wizard.get_cleaned_data_for_step(LOCATION) or {}
    # if the user selected abroad, show the international form
    return cleaned_data.get("location") == "abroad"


def show_domestic_site_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(LOCATION) or {}
    # if the user selected united_kingdom, show the uk form
    return cleaned_data.get("location") == "united_kingdom"


def show_add_site_confirmation_form(wizard):
    # check if a site has already been added with the same postcode
    cleaned_data = wizard.get_cleaned_data_for_step(UK_ADDRESS) or {}
    postcode = cleaned_data.get("postcode")
    if not postcode:
        return False
    existing_sites = get_sites(wizard.request, wizard.request.session["organisation"], postcode=postcode)
    return len(existing_sites) > 0


class NewSiteWizardView(SessionWizardView, LoginRequiredMixin):
    template_name = "core/form-wizard.html"
    form_list = [
        (LOCATION, site_forms.NewSiteLocationForm),
        (UK_ADDRESS, site_forms.NewSiteUKAddressForm),
        (INTERNATIONAL_ADDRESS, site_forms.NewSiteInternationalAddressForm),
        (CONFIRM, site_forms.NewSiteConfirmForm),
        (ASSIGN_USERS, site_forms.NewSiteAssignUsersForm),
    ]

    def render_next_step(self, form, **kwargs):
        if self.steps.current == "confirm":
            if not str_to_bool(form.cleaned_data["are_you_sure"]):
                return redirect(reverse("organisation:sites:sites"))
        return super().render_next_step(form, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["back_link_url"] = reverse("organisation:sites:sites")
        return context

    def get_form_kwargs(self, step):  # noqa pylint incorrectly flagging this
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        if step == CONFIRM:
            if self.storage.get_step_data("uk_address"):
                kwargs["postcode"] = self.storage.get_step_data("uk_address").get("uk_address-postcode")
        return kwargs

    def done(self, form_list, **kwargs):
        # merge all answers into one dictionary
        form_data = [form.serialized_data for form in form_list]
        site_data = {key: value for f in form_data for key, value in f.items()}
        organisation_id = str(self.request.session["organisation"])
        response = post_sites(self.request, organisation_id, site_data)
        json = response.json()
        return redirect(reverse("organisation:sites:site", kwargs={"pk": json["site"]["id"]}))


class ViewSite(TemplateView):
    def get(self, request, *args, **kwargs):
        organisation_id = str(request.session["organisation"])
        site = get_site(request, organisation_id, kwargs["pk"])
        organisation = get_organisation(request, organisation_id)

        context = {
            "site": site,
            "organisation": organisation,
        }
        return render(request, "organisation/sites/site.html", context)


class EditSiteName(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        site = get_site(request, request.session["organisation"], self.object_pk)
        self.data = site
        self.form = edit_site_name_form(site)
        self.action = update_site
        self.success_url = reverse("organisation:sites:site", kwargs={"pk": self.object_pk})


class EditSiteRecordsLocation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        site = get_site(request, request.session["organisation"], self.object_pk)
        in_uk = site["address"]["country"]["id"] == "GB"
        self.form = site_records_location(request, in_uk=in_uk, is_editing=True)
        self.action = update_site
        self.success_url = reverse("organisation:sites:site", kwargs={"pk": self.object_pk})
