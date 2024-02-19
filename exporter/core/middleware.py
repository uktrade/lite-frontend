import logging

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from .constants import OrganisationStatus
from core.exceptions import ServiceError
from core.views import error_page
from exporter.organisation.members.services import get_user

logger = logging.getLogger(__name__)


class OrganisationRedirectMiddleWare:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        # whitelist logout
        if request.path == reverse("auth:logout"):
            return self.get_response(request)
        if not request.path == reverse("core:register_an_organisation_confirm"):
            # Check if the user is allowed to make API calls and logged in
            if request.authbroker_client.token and request.session.get("user_token"):
                if self.is_organisations_in_status(request, OrganisationStatus.REVIEW):
                    # An application is still in review
                    return redirect(reverse("core:register_an_organisation_confirm") + "?animate=True")
        # If the user doesn't have a LITE account don't allow them to homepage since they need to register
        if request.path == reverse("core:home"):
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
