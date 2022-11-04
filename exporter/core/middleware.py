import logging

from django.conf import settings
from django.shortcuts import redirect
from lite_forms.generators import error_page

from core.exceptions import ServiceError
from .constants import OrganisationStatus

from django.urls import reverse_lazy, reverse
from exporter.organisation.members.services import get_user

logger = logging.getLogger(__name__)


class OrganisationRedirectMiddleWare:
    ignore_paths = [
        reverse_lazy("core:register_an_organisation_triage"),
        reverse_lazy("core:register_an_organisation_confirm"),
        reverse_lazy("core:register_name"),
        reverse_lazy("core:home"),
        reverse_lazy("auth:logout"),
    ]
    home_url = reverse_lazy("core:home")
    register_triage = reverse_lazy("core:register_an_organisation_triage")

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        # skip for register-an-organisation log-out and other whitelist urls
        # Check if the user is allowed to make API calls
        if request.path == reverse("auth:logout"):
            return self.get_response(request)
        if not request.path == reverse("core:register_an_organisation_confirm"):
            if request.authbroker_client.token and request.session.get("user_token"):
                if self.is_organisations_in_status(request, OrganisationStatus.REVIEW):
                    # An application is still in review
                    return redirect(reverse("core:register_an_organisation_confirm") + "?animate=True")
        if request.path == self.home_url:
            if request.authbroker_client.token and not request.session.get("user_token"):
                if not (request.session.get("first_name") or request.session.get("second_name")):
                    return redirect(reverse("core:register_name"))
                else:
                    return redirect(reverse("core:register_an_organisation_triage"))
        return self.get_response(request)

    def is_organisations_in_status(self, request, status):
        # TODO stream line this call to one call to retrieve all status
        organisations = get_user(request, params={status: True})["organisations"]
        if not organisations:
            return False
        return any(org.get("status", {}).get("key") == status for org in organisations)


class ServiceErrorHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if not isinstance(exception, ServiceError):
            return None

        logger.error(
            exception.log_message,
            exception.status_code,
            exception.response,
            exc_info=True,
        )
        if settings.DEBUG:
            raise exception
        return error_page(request, exception.user_message)
