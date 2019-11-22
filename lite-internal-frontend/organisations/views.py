from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from core.helpers import convert_dict_to_query_params
from lite_content.lite_internal_frontend import strings
from lite_forms.generators import form_page
from lite_forms.submitters import submit_paged_form
from organisations.forms import register_business_forms, register_hmrc_organisation_forms
from organisations.services import get_organisations, get_organisations_sites, get_organisation, post_organisations


class OrganisationList(TemplateView):
    """
    Show all organisations.
    """

    def get(self, request, **kwargs):
        search_term = request.GET.get("search_term", "").strip()
        org_type = request.GET.get("org_type", "").strip()

        params = {"page": int(request.GET.get("page", 1))}
        if search_term:
            params["search_term"] = search_term
        if org_type:
            params["org_type"] = org_type

        organisations, _ = get_organisations(request, convert_dict_to_query_params(params))

        context = {
            "data": organisations,
            "title": "Organisations",
            "page": params.pop("page"),
            "params": params,
            "params_str": convert_dict_to_query_params(params),
        }
        return render(request, "organisations/index.html", context)


class OrganisationDetail(TemplateView):
    """
    Show an organisation.
    """

    def get(self, request, **kwargs):
        organisation_pk = str(kwargs["pk"])
        data, _ = get_organisation(request, organisation_pk)
        sites, _ = get_organisations_sites(request, organisation_pk)

        context = {
            "organisation": data,
            "title": data["name"],
            "sites": sites["sites"],
        }
        return render(request, "organisations/organisation.html", context)


class HMRCList(TemplateView):
    def get(self, request, **kwargs):
        data, _ = get_organisations(request, convert_dict_to_query_params({"org_type": "hmrc"}))
        context = {
            "data": data,
            "title": "Organisations",
        }
        return render(request, "organisations/hmrc/index.html", context)


class RegisterBusiness(TemplateView):
    forms = None

    def dispatch(self, request, *args, **kwargs):
        individual = request.POST.get("type") == "individual"
        name = request.POST.get("name")
        self.forms = register_business_forms(individual, name) if name else register_business_forms(individual)

        return super(RegisterBusiness, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, _ = submit_paged_form(request, self.forms, post_organisations)

        if response:
            return response

        messages.success(request, strings.ORGANISATION_CREATION_SUCCESS)
        return redirect("organisations:organisations")


class RegisterHMRC(TemplateView):
    forms = None

    def dispatch(self, request, *args, **kwargs):
        name = request.POST.get("name")
        self.forms = register_hmrc_organisation_forms(name) if name else register_hmrc_organisation_forms()

        return super(RegisterHMRC, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return form_page(request, self.forms.forms[0])

    def post(self, request, **kwargs):
        response, _ = submit_paged_form(request, self.forms, post_organisations)

        if response:
            return response

        messages.success(request, strings.HMRC_ORGANISATION_CREATION_SUCCESS)
        return redirect("organisations:hmrc")
