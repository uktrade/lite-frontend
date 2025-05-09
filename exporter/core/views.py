from json import JSONDecodeError

from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect

from exporter.applications.services import (
    get_applications_require_serial_numbers,
    has_existing_applications_and_licences_and_nlrs,
)
from exporter.auth.services import authenticate_exporter_user

from exporter.core.forms import RegisterNameForm

from exporter.core.services import (
    get_notifications,
    get_organisation,
    get_signature_certificate,
)

from core.auth.utils import get_profile
from lite_content.lite_exporter_frontend import generic
from lite_forms.components import BackLink
from lite_forms.generators import success_page
from lite_forms.helpers import conditional
from exporter.organisation.members.services import get_user
from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin


class Home(TemplateView):
    def _applications_with_missing_serial_numbers(self, request):
        response = get_applications_require_serial_numbers(request)
        application_ids = [application["id"] for application in response["results"]]
        return len(response["results"]), application_ids

    def get(self, request, **kwargs):
        if not request.authbroker_client.token:
            return render(request, "core/start-gov-uk.html")
        try:
            user = get_user(request)
            user_permissions = user["role"]["permissions"]
        except (JSONDecodeError, TypeError, KeyError):
            return redirect("auth:login")
        notifications, _ = get_notifications(request)
        require_serials_count, require_serials_ids = self._applications_with_missing_serial_numbers(request)
        organisation = get_organisation(request, str(request.session["organisation"]))
        existing = has_existing_applications_and_licences_and_nlrs(request)

        context = {
            "organisation": organisation,
            "user_data": user,
            "notifications": notifications,
            "application_notification_count": self.get_application_notification_count(notifications),
            "missing_serials_count": require_serials_count,
            "missing_serials_id": require_serials_ids[0] if require_serials_ids else None,
            "existing": existing,
            "user_permissions": user_permissions,
            "FEATURE_FLAG_ONLY_ALLOW_SIEL": settings.FEATURE_FLAG_ONLY_ALLOW_SIEL,
            "FEATURE_FLAG_ALLOW_CLC_QUERY_AND_PV_GRADING": settings.FEATURE_FLAG_ALLOW_CLC_QUERY_AND_PV_GRADING,
            "SURVEY_URL": settings.SURVEY_URL,
        }

        return render(request, "core/hub.html", context)

    def get_application_notification_count(self, notifications):
        notification_data = notifications.get("notifications", {})
        return notification_data.get("application", 0) + notification_data.get("security_clearance", 0)


class RegisterAnOrganisationConfirmation(TemplateView):
    def get(self, request, *args, **kwargs):
        organisation = get_user(request, params={"in_review": True})["organisations"][0]
        organisation_name = organisation["name"]
        organisation_status = organisation["status"]["key"]

        if organisation_status != "in_review":
            raise Http404

        return success_page(
            request=request,
            title=f"You've successfully registered: {organisation_name}",
            secondary_title="We're currently processing your application.",
            description="",
            what_happens_next=[
                "Export Control Joint Unit (ECJU) is processing your request for an export control account. "
                "We'll send you an email when we've made a final decision."
            ],
            links={},
            back_link=conditional(
                request.GET.get("show_back_link", False),
                BackLink(generic.BACK, reverse_lazy("core:select_organisation")),
            ),
            animated=True,
            additional_context={"user_in_limbo": True},
        )


class RegisterName(LoginRequiredMixin, FormView):
    template_name = "core/form.html"
    form_class = RegisterNameForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = self.form_class.Layout.TITLE
        return context

    def get_success_url(self):
        return resolve_url(settings.LOGIN_URL)

    def dispatch(self, request, *args, **kwargs):
        if self.request.session.get("first_name") and self.request.session.get("last_name"):
            return HttpResponseRedirect(resolve_url(settings.LOGIN_URL))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        profile = get_profile(self.request.authbroker_client)
        profile.update(
            {
                "user_profile": {
                    "first_name": form.cleaned_data["first_name"],
                    "last_name": form.cleaned_data["last_name"],
                }
            },
        )
        # attempt to update user
        authenticate_exporter_user(self.request, profile)
        # Hold in session
        self.request.session["first_name"] = form.cleaned_data["first_name"]
        self.request.session["last_name"] = form.cleaned_data["last_name"]
        self.request.session["email"] = profile["email"]

        return super().form_valid(form)


class SignatureHelp(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "core/signature-help.html", {})


class CertificateDownload(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return get_signature_certificate(request)


def handler403(request, exception):
    return error_page(request, title="Forbidden", description=exception, show_back_link=True)


class PrivacyNotice(TemplateView):
    template_name = "core/privacy_notice.html"


class HelpSupportView(TemplateView):
    template_name = "core/help_support.html"
