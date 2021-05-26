from logging import getLogger

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import View

from core.auth import views as auth_views
from exporter.auth.services import authenticate_exporter_user
from lite_forms.generators import error_page
from exporter.organisation.members.services import get_user


logger = getLogger(__name__)


class AuthCallbackView(auth_views.AbstractAuthCallbackView, View):
    def authenticate_user(self):
        # Great SSO is adding social login. We do not want users
        # to authenticate with Great SSO using e.g. LinkedIn.
        # This seems like as good a place as any to stop this.
        # P.S. Great SSO has added social_login flag in user profiles.
        logger.warn("Authenticating exporter with Great SSO: %s", self.user_profile)
        if self.user_profile.get("social_login", False):
            logger.error("Exporter tried using Great social auth: %s", self.user_profile)
            return {"errors": "We do not support social login. Please use a secure email."}, 403
        return authenticate_exporter_user(self.request, self.user_profile)

    def handle_failure(self, data, status_code):
        if status_code in {400, 403}:
            return error_page(self.request, data["errors"])
        elif status_code == 401:
            return redirect("core:register_an_organisation_triage")

    def handle_success(self, data, status_code):
        self.request.session["first_name"] = data["first_name"]
        self.request.session["last_name"] = data["last_name"]
        self.request.session["user_token"] = data["token"]
        self.request.session["lite_api_user_id"] = data["lite_api_user_id"]
        self.request.session["email"] = self.user_profile["email"]
        return redirect(self.get_success_url())

    def get_success_url(self):
        user = get_user(self.request)
        if not user["organisations"]:
            return reverse("core:register_an_organisation_triage")
        elif len(user["organisations"]) == 1:
            organisation = user["organisations"][0]
            if organisation["status"]["key"] != "in_review":
                self.request.session["organisation"] = user["organisations"][0]["id"]
            else:
                return reverse("core:register_an_organisation_confirm")
        elif len(user["organisations"]) > 1:
            return reverse("core:pick_organisation")
        return settings.LOGIN_REDIRECT_URL
