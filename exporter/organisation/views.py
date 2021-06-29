from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from core.helpers import format_date
from exporter.core.constants import Permissions
from exporter.core.objects import Tab
from exporter.core.services import get_organisation
from lite_content.lite_exporter_frontend.organisation import Tabs
from lite_forms.helpers import conditional
from exporter.organisation.roles.services import get_user_permissions
from exporter.goods.forms import attach_firearm_dealer_certificate_form
from exporter.organisation import forms
from exporter.organisation.services import post_document_on_organisation, get_document_on_organisation
from core.auth.views import LoginRequiredMixin
from lite_forms.generators import form_page
from s3chunkuploader.file_handler import s3_client


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


class DocumentOnOrganisation(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, pk):
        organisation_id = str(self.request.session["organisation"])
        response = get_document_on_organisation(request=self.request, organisation_id=organisation_id, document_id=pk)
        document_on_organisation = response.json()
        signed_url = s3_client().generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": document_on_organisation["document"]["s3_key"]},
            ExpiresIn=15,
        )
        return signed_url


class AbstractOrganisationUpload(LoginRequiredMixin, TemplateView):
    document_type = None

    def form_function(self, back_url):
        raise NotImplementedError

    def get(self, request, **kwargs):
        form = self.form_function(back_url=reverse("organisation:details"))  # pylint: disable=E1102
        return form_page(request, form)

    def post(self, request, **kwargs):
        organisation_id = str(request.session["organisation"])
        data = {
            "expiry_date": format_date(request.POST, "expiry_date_"),
            "reference_code": self.request.POST["reference_code"],
            "document_type": self.document_type,
        }

        file = request.FILES.get("file")
        if file:
            data["document"] = {
                "name": getattr(file, "original_name", file.name),
                "s3_key": file.name,
                "size": int(file.size // 1024) if file.size else 0,  # in kilobytes
            }

        response = post_document_on_organisation(request=request, organisation_id=organisation_id, data=data)

        if "errors" in response.json():
            form = self.form_function(back_url=reverse("organisation:details"))
            errors = response.json()["errors"]
            return form_page(request, form, errors=errors)

        return redirect(reverse("organisation:details"))


class UploadFirearmsCertificate(AbstractOrganisationUpload):
    form_function = staticmethod(attach_firearm_dealer_certificate_form)
    document_type = "rfd-certificate"


class UploadSectionFiveCertificate(AbstractOrganisationUpload):
    form_function = staticmethod(forms.attach_section_five_certificate_form)
    document_type = "section-five-certificate"
