import logging
from django.shortcuts import redirect
from django.urls import reverse

from exporter.organisation.members.services import get_user

logger = logging.getLogger(__name__)

ignore_paths = ["/register-an-organisation/draft-confirmation/", "/auth/logout/", "/register-an-organisation/confirm/"]


class OrganisationRedirectMiddleWare:
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        # skip for register-an-organisation log-out and other whitelist urls
        if request.path in ignore_paths or request.path_info.startswith("/register-an-organisation/edit/"):
            return self.get_response(request)

        # Check if the user is allowed to make API calls
        if request.authbroker_client.token and request.session.get("user_token"):
            draft_organisations = get_user(request, params={"draft": True})["organisations"]
            # TODO stream line this call to one call to retrieve all status
            if len(draft_organisations) and draft_organisations[0]["status"]["key"] == "draft":
                # Application is still in draft state
                return redirect("core:register_draft_confirm")
            else:
                # Application is in review state
                review_organisations = get_user(request, params={"in_review": True})["organisations"]
                if len(review_organisations) and review_organisations[0]["status"]["key"] == "in_review":
                    return redirect(reverse("core:register_an_organisation_confirm") + "?animate=True")
        return self.get_response(request)
