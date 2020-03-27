from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from core.services import get_organisation
from lite_forms.views import MultiFormView, SingleFormView
from organisation.sites.forms import new_site_forms, edit_site_name_form
from organisation.sites.services import get_site, post_sites, update_site, get_sites
from organisation.views import OrganisationView


class Sites(OrganisationView):
    template_name = "sites/index"

    def get_additional_context(self):
        return {"sites": get_sites(self.request, self.organisation_id)}


class NewSite(MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = request.user.organisation
        self.forms = new_site_forms(request)
        self.action = post_sites

    def get_success_url(self):
        pk = self.get_validated_data()["site"]["id"]
        return reverse("organisation:sites:site", kwargs={"pk": pk})


class ViewSite(TemplateView):
    def get(self, request, *args, **kwargs):
        organisation_id = str(request.user.organisation)
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
        site = get_site(request, request.user.organisation, self.object_pk)
        self.data = site
        self.form = edit_site_name_form(site)
        self.action = update_site
        self.success_url = reverse("organisation:sites:site", kwargs={"pk": self.object_pk})
