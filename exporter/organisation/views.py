from http import HTTPStatus

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView, RedirectView, View

from lite_content.lite_exporter_frontend.organisation import Tabs
from lite_forms.helpers import conditional

from core.auth.views import LoginRequiredMixin
from core.constants import OrganisationDocumentType
from core.decorators import expect_status
from core.helpers import (
    get_document_data,
    stream_document_response,
)

from exporter.core.constants import Permissions
from exporter.core.objects import Tab
from exporter.core.services import get_organisation
from exporter.organisation.roles.services import get_user_permissions
from exporter.organisation import forms
from exporter.organisation.services import (
    get_document_on_organisation,
    post_document_on_organisation,
    stream_document_on_organisation,
)


class OrganisationView(TemplateView):
    organisation_id = None
    organisation = None
    additional_context = {}

    def get_additional_context(self):
        return self.additional_context

    def get(self, request, **kwargs):
        self.organisation_id = str(request.session["organisation"])
        self.organisation = get_organisation(request, self.organisation_id)

        user_permissions = kwargs.get("permissions", get_user_permissions(request))
        can_administer_sites = Permissions.ADMINISTER_SITES in user_permissions
        can_administer_roles = Permissions.EXPORTER_ADMINISTER_ROLES in user_permissions

        documents = {item["document_type"].replace("-", "_"): item for item in self.organisation.get("documents", [])}
        context = {
            "organisation": self.organisation,
            "can_administer_sites": can_administer_sites,
            "can_administer_roles": can_administer_roles,
            "user_permissions": user_permissions,
            "tabs": [
                Tab("members", Tabs.MEMBERS, reverse_lazy("organisation:members:members")),
                conditional(can_administer_sites, Tab("sites", Tabs.SITES, reverse_lazy("organisation:sites:sites"))),
                conditional(can_administer_roles, Tab("roles", Tabs.ROLES, reverse_lazy("organisation:roles:roles"))),
                Tab("details", Tabs.DETAILS, reverse_lazy("organisation:details")),
            ],
            "documents": documents,
            **self.get_additional_context(),
        }
        return render(request, f"organisation/{self.template_name}.html", context)


class RedirectToMembers(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("organisation:members:members")


class Details(LoginRequiredMixin, OrganisationView):
    template_name = "details/index"


class DocumentOnOrganisation(LoginRequiredMixin, View):
    @expect_status(
        HTTPStatus.OK,
        "Error downloading document",
        "Unexpected error downloading document",
    )
    def stream_document_on_organisation(self, request, organisation_id, pk):
        return stream_document_on_organisation(request, organisation_id, pk)

    def get(self, request, pk):
        organisation_id = str(self.request.session["organisation"])
        response = get_document_on_organisation(request=self.request, organisation_id=organisation_id, document_id=pk)
        document_on_organisation = response.json()

        api_response, _ = self.stream_document_on_organisation(
            request,
            organisation_id,
            document_on_organisation["id"],
        )

        return stream_document_response(api_response)


class AbstractOrganisationUpload(LoginRequiredMixin, FormView):
    document_type = None

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(back_link_url=reverse("organisation:details"), *args, **kwargs)

    def form_valid(self, form):
        organisation_id = str(self.request.session["organisation"])

        data = {**form.cleaned_data}
        file = data.pop("file")

        data["document_type"] = self.document_type
        data["document"] = get_document_data(file)

        formatted_date = data["expiry_date"].isoformat()
        data["expiry_date"] = formatted_date

        post_document_on_organisation(request=self.request, organisation_id=organisation_id, data=data)
        return super().form_valid(form)


class UploadFirearmsCertificate(AbstractOrganisationUpload):
    template_name = "core/form.html"
    form_class = forms.UploadFirearmsCertificateForm
    success_url = reverse_lazy("organisation:details")
    document_type = OrganisationDocumentType.RFD_CERTIFICATE

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(
            form_action_url=reverse("organisation:upload-firearms-certificate"), *args, **kwargs
        )
        context["form_title"] = self.form_class.Layout.TITLE
        return context


class UploadSectionFiveCertificate(AbstractOrganisationUpload):
    template_name = "core/form.html"
    form_class = forms.UploadSectionFiveCertificateForm
    success_url = reverse_lazy("organisation:details")
    document_type = "section-five-certificate"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(
            form_action_url=reverse("organisation:upload-section-five-certificate"), *args, **kwargs
        )
        context["form_title"] = self.form_class.Layout.TITLE
        return context
