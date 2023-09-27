import logging
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import View, RedirectView

from core.auth import views as auth_views
from exporter.auth.services import authenticate_exporter_user
from lite_forms.generators import error_page
from exporter.organisation.members.services import get_user
from authlib.oauth2.rfc7523 import PrivateKeyJWT
from core.ip_filter import get_client_ip

logger = logging.getLogger(__name__)


class AuthCallbackView(auth_views.AbstractAuthCallbackView, View):
    def authenticate_user(self):
        profile = self.user_profile
        logger.info(
            "Authentication:Service: %s : authenticate user in lite with profile: %s: client_ip:%s ",
            settings.AUTHBROKER_AUTHORIZATION_URL,
            profile,
            get_client_ip(self.request),
        )
        return authenticate_exporter_user(self.request, profile)

    def handle_failure(self, data, status_code):
        if status_code == 400:
            return error_page(self.request, data["errors"])
        elif status_code == 401:
            # No user in lite DB we need to capture their name
            if not (self.request.session.get("first_name") or self.request.session.get("second_name")):
                return redirect(reverse("core:register_name"))
            else:
                return redirect("core:register_an_organisation_triage")

    def handle_success(self, data, status_code):
        logger.info(
            "Authentication:Service: %s : user login successful  %s",
            settings.AUTHBROKER_AUTHORIZATION_URL,
            self.user_profile,
        )
        self.request.session["user_token"] = data["token"]
        self.request.session["lite_api_user_id"] = data["lite_api_user_id"]
        self.request.session["email"] = self.user_profile["email"]
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
                self.request.session["organisation_name"] = user["organisations"][0]["name"]
            else:
                return reverse("core:register_an_organisation_confirm")
        elif len(user["organisations"]) > 1:
            return reverse("core:select_organisation")
        return settings.LOGIN_REDIRECT_URL

    def fetch_token(self, request, auth_code):
        logger.info(
            "Authentication:Service: %s : fetching token for login auth_code %s: client_ip:%s",
            settings.AUTHBROKER_AUTHORIZATION_URL,
            auth_code,
            get_client_ip(self.request),
        )

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


class AuthLogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        """
        In the real GovOne SSO, it handles redirection, not this codebase.

        For this mock implementation, hard code redirecting to /

        :param args:
        :param kwargs:
        :return:
        """
        logger.info(
            "Authentication:Service: %s: logout user %s: client_ip: %s",
            settings.AUTHBROKER_AUTHORIZATION_URL,
            settings.LOGOUT_URL,
            get_client_ip(self.request),
        )
        redirect_url = self.request.build_absolute_uri("/")
        if self.request.authbroker_client.token:
            if self.request.authbroker_client.token.get("id_token"):
                # if we have an ID token then the logout call to SSO service will require this.
                logout_query = urlencode(
                    {
                        "id_token_hint": self.request.authbroker_client.token["id_token"],
                        "post_logout_redirect_uri": self.request.build_absolute_uri("/"),
                    }
                )
                redirect_url = settings.LOGOUT_URL + f"?{logout_query}"
        else:
            # We not even logged redirect to home page
            redirect_url = self.request.build_absolute_uri("/")
        self.request.session.flush()
        return redirect_url
