from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from conf.constants import Permission
from core.helpers import convert_dict_to_query_params
from core.objects import Tab
from core.services import get_user_permissions
from lite_content.lite_internal_frontend import strings
from lite_content.lite_internal_frontend.organisations import OrganisationsPage, OrganisationPage
from lite_forms.components import FiltersBar, TextInput, Select, Option
from lite_forms.views import MultiFormView, SingleFormView
from organisations.forms import (
    register_organisation_forms,
    register_hmrc_organisation_forms,
    edit_commercial_form,
    edit_individual_form,
)
from organisations.services import (
    get_organisations,
    get_organisation_sites,
    get_organisation,
    post_organisations,
    put_organisation,
    get_organisation_members,
    post_hmrc_organisations,
)


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

        filters = FiltersBar(
            [
                TextInput(name="search_term", title=OrganisationsPage.Filters.NAME),
                Select(
                    name="org_type",
                    title=OrganisationsPage.Filters.TYPE,
                    options=[
                        Option("individual", OrganisationsPage.Filters.Types.INDIVIDUAL),
                        Option("commercial", OrganisationsPage.Filters.Types.COMMERCIAL),
                        Option("hmrc", OrganisationsPage.Filters.Types.HMRC),
                    ],
                ),
            ]
        )

        context = {
            "data": organisations,
            "page": params.pop("page"),
            "params_str": convert_dict_to_query_params(params),
            "filters": filters,
            "search_term": params.get("search_term", ""),
            "can_manage_organisations": Permission.MANAGE_ORGANISATIONS.value in get_user_permissions(request),
        }
        return render(request, "organisations/index.html", context)


class OrganisationView(TemplateView):
    organisation_id = None
    organisation = None
    additional_context = {}

    def get_additional_context(self):
        return self.additional_context

    def get(self, request, **kwargs):
        self.organisation_id = kwargs["pk"]
        self.organisation = get_organisation(request, self.organisation_id)

        context = {
            "organisation": self.organisation,
            "tabs": [
                Tab(
                    "details",
                    OrganisationPage.Details.TITLE,
                    reverse_lazy("organisations:organisation", kwargs={"pk": self.organisation_id}),
                ),
                Tab(
                    "members",
                    OrganisationPage.Members.TITLE,
                    reverse_lazy("organisations:organisation_members", kwargs={"pk": self.organisation_id}),
                ),
                Tab(
                    "sites",
                    OrganisationPage.Sites.TITLE,
                    reverse_lazy("organisations:organisation_sites", kwargs={"pk": self.organisation_id}),
                ),
            ],
        }
        context.update(self.get_additional_context())
        return render(request, f"organisations/organisation/{self.template_name}.html", context)


class OrganisationDetails(OrganisationView):
    template_name = "details"


class OrganisationMembers(OrganisationView):
    template_name = "members"

    def get_additional_context(self):
        return {"members": get_organisation_members(self.request, self.organisation_id)}


class OrganisationSites(OrganisationView):
    template_name = "sites"

    def get_additional_context(self):
        return {"sites": get_organisation_sites(self.request, self.organisation_id)}


class RegisterOrganisation(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = register_organisation_forms(request)
        self.action = post_organisations
        self.success_message = strings.ORGANISATION_CREATION_SUCCESS
        self.success_url = reverse("organisations:organisations")


class RegisterHMRC(MultiFormView):
    def init(self, request, **kwargs):
        self.forms = register_hmrc_organisation_forms()
        self.action = post_hmrc_organisations
        self.success_message = strings.HMRC_ORGANISATION_CREATION_SUCCESS
        self.success_url = reverse("organisations:organisations")


class EditOrganisation(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        organisation = get_organisation(request, str(self.object_pk))
        self.data = organisation
        self.action = put_organisation
        self.success_url = reverse_lazy("organisations:organisation", kwargs={"pk": self.object_pk})

    def get_form(self):
        user_permissions = get_user_permissions(self.request)
        permission_to_edit_org_name = (
            Permission.MANAGE_ORGANISATIONS.value in user_permissions
            and Permission.REOPEN_CLOSED_CASES.value in user_permissions
        )
        are_fields_optional = "address" in self.data["primary_site"]["address"].get("address_line_1")
        form = edit_commercial_form if self.data["type"]["key"] == "commercial" else edit_individual_form

        return form(self.data, permission_to_edit_org_name, are_fields_optional)
