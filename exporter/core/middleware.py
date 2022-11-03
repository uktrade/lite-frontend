import logging
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework.reverse import reverse_lazy
from exporter.organisation.members.services import get_user
from .constants import OrganisationStatus
from django.conf import settings

from lite_forms.generators import error_page

from core.exceptions import ServiceError


logger = logging.getLogger(__name__)


ignore_paths = [
    reverse_lazy("core:register_draft_confirm"),
    reverse_lazy("auth:logout"),
    reverse_lazy("core:register_an_organisation_confirm"),
]


class OrganisationRedirectMiddleWare:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        # skip for register-an-organisation log-out and other whitelist urls
        if request.path in ignore_paths or request.path_info.startswith("/register-an-organisation/edit/"):
            return self.get_response(request)

        # Check if the user is allowed to make API calls
        if request.authbroker_client.token and request.session.get("user_token"):
            if self.is_organisations_in_status(request, OrganisationStatus.DRAFT):
                # An application is still in draft state
                return redirect("core:register_draft_confirm")
            else:
                # An application is in review state
                if self.is_organisations_in_status(request, OrganisationStatus.REVIEW):
                    return redirect(reverse("core:register_an_organisation_confirm") + "?animate=True")
        return self.get_response(request)

    def is_organisations_in_status(self, request, status):
        # TODO stream line this call to one call to retrieve all status
        organisations = get_user(request, params={status: True})["organisations"]
        if not organisations:
            return False
        return any(org["status"]["key"] == status for org in organisations)


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
