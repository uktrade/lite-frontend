from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import View

from core.auth import views as auth_views
from exporter.auth.services import authenticate_exporter_user
from lite_forms.generators import error_page
from exporter.organisation.members.services import get_user
from authlib.oauth2.rfc7523 import PrivateKeyJWT


class AuthCallbackView(auth_views.AbstractAuthCallbackView, View):
    def authenticate_user(self):
        profile = self.user_profile
        if settings.FEATURE_FLAG_GOVUK_SIGNIN_ENABLED:
            profile["no_profile_login"] = True
        return authenticate_exporter_user(self.request, profile)

    def handle_failure(self, data, status_code):
        if status_code == 400:
            return error_page(self.request, data["errors"])
        elif status_code == 401:
            # No user in lite DB we need to capture their name
            if (
                not (self.request.session.get("first_name") or self.request.session.get("second_name"))
                and settings.FEATURE_FLAG_GOVUK_SIGNIN_ENABLED
            ):
                return redirect(reverse("core:register_name"))
            else:
                return redirect("core:register_an_organisation_triage")

    def handle_success(self, data, status_code):

        self.request.session["user_token"] = data["token"]
        self.request.session["lite_api_user_id"] = data["lite_api_user_id"]
        self.request.session["email"] = self.user_profile["email"]
        if settings.FEATURE_FLAG_GOVUK_SIGNIN_ENABLED:
            if not (data["first_name"] and data["last_name"]):
                # We have a registered user with no first_name and last_name
                # Once all Great users have transferred to new gov.uk this can be removed.
                return redirect(reverse("core:register_name"))
        self.request.session["first_name"] = data["first_name"]
        self.request.session["last_name"] = data["last_name"]
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

    def fetch_token(self, request, auth_code):
        if settings.FEATURE_FLAG_GOVUK_SIGNIN_ENABLED:
            request.authbroker_client.token_endpoint_auth_method = PrivateKeyJWT(
                token_endpoint=settings.AUTHBROKER_TOKEN_URL
            )

        return request.authbroker_client.fetch_token(
            url=settings.AUTHBROKER_TOKEN_URL,
            code=auth_code,
            client_secret=settings.AUTHBROKER_CLIENT_SECRET,
            grant_type="authorization_code",
            client_assertion_type="urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            client_id=settings.AUTHBROKER_CLIENT_ID,
        )
