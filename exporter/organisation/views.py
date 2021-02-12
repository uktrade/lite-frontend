from s3chunkuploader.file_handler import S3FileUploadHandler

from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, RedirectView
from django.urls import reverse

from exporter.applications.helpers.date_fields import format_date
from exporter.core.constants import Permissions
from exporter.core.objects import Tab
from exporter.core.services import get_organisation
from lite_content.lite_exporter_frontend.organisation import Tabs
from lite_forms.helpers import conditional
from exporter.organisation.roles.services import get_user_permissions

from exporter.organisation import forms
from exporter.organisation.services import post_organisation_documents
from core.auth.views import LoginRequiredMixin
from lite_forms.generators import form_page


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
            "documents": {item["document_type"].replace("-", "_"): item for item in self.organisation["documents"]},
            **self.get_additional_context(),
        }
        return render(request, f"organisation/{self.template_name}.html", context)


class RedirectToMembers(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("organisation:members:members")


class Details(LoginRequiredMixin, OrganisationView):
    template_name = "details/index"


@method_decorator(csrf_exempt, "dispatch")
class AbstractOrganisationUpload(TemplateView):
    form_function = None
    document_type = None

    def get(self, request, **kwargs):
        form = self.form_function(back_url=reverse("organisation:details"))
        return form_page(request, form)

    def handle_s3_upload(self):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(self.request))

    @csrf_exempt
    def post(self, request, **kwargs):
        self.handle_s3_upload()

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

        post_organisation_documents(request=request, organisation_id=organisation_id, data=data)

        return redirect(reverse("organisation:details"))


class UploadFirearmsCertificate(AbstractOrganisationUpload):
    form_function = staticmethod(forms.attach_firearm_dealer_certificate_form)
    document_type = "rfd-certificate"


class UploadSectionFiveCertificate(AbstractOrganisationUpload):
    form_function = staticmethod(forms.attach_section_five_certificate_form)
    document_type = "section-five-certificate"
