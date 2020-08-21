import logging

import sentry_sdk

from django.conf import settings
from django.http import HttpResponseServerError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import View

from core.auth import views as auth_views
from exporter.auth.services import authenticate_exporter_user
from exporter.auth.utils import get_client, AUTHORISATION_URL, TOKEN_SESSION_KEY, TOKEN_URL, get_profile
from lite_forms.generators import error_page
from exporter.organisation.members.services import get_user


class AuthView(auth_views.AuthView):
    """
    Auth wrapper which connects to api
    """

    AUTHORIZATION_URL = AUTHORISATION_URL
    TOKEN_SESSION_KEY = TOKEN_SESSION_KEY

    def get_client(self):
        return get_client(self.request)


class AuthCallbackView(View):
    """
    Auth process for exporter, only called by 'great sso'
    """

    def get(self, request, *args, **kwargs):
        logging.info("Login callback received from GREAT SSO")

        auth_code = request.GET.get("code", None)

        if not auth_code:
            return redirect(reverse_lazy("auth:login"))

        state = self.request.session.get(TOKEN_SESSION_KEY + "_oauth_state", None)

        if not state:
            return HttpResponseServerError()

        try:
            token = get_client(self.request).fetch_token(
                TOKEN_URL, client_secret=settings.AUTHBROKER_CLIENT_SECRET, code=auth_code
            )

            self.request.session[TOKEN_SESSION_KEY] = dict(token)

            del self.request.session[TOKEN_SESSION_KEY + "_oauth_state"]

        # NOTE: the BaseException will be removed or narrowed at a later date. The try/except block is
        # here due to reports of the app raising a 500 if the url is copied.  Current theory is that
        # somehow the url with the authcode is being copied, which would cause `fetch_token` to raise
        # an exception. However, looking at the fetch_code method, I'm not entirely sure what exceptions it
        # would raise in this instance.
        except BaseException as base_exception:
            sentry_sdk.capture_exception(base_exception)

        profile = get_profile(get_client(self.request))

        response, status_code = authenticate_exporter_user(request, profile)

        if status_code == 400:
            return error_page(request, response.get("errors")[0])

        if status_code == 200:

            request.session["first_name"] = response["first_name"]
            request.session["last_name"] = response["last_name"]
            request.session["user_token"] = response["token"]
            request.session["lite_api_user_id"] = response["lite_api_user_id"]
        elif status_code == 401:
            return redirect("core:register_an_organisation_triage")

        user_dict = get_user(request)

        if len(user_dict["organisations"]) == 0:
            return redirect("core:register_an_organisation_triage")
        elif len(user_dict["organisations"]) == 1:
            organisation = user_dict["organisations"][0]
            if organisation["status"]["key"] != "in_review":
                request.session["organisation"] = user_dict["organisations"][0]["id"]
            else:
                return redirect("core:register_an_organisation_confirm")
        elif len(user_dict["organisations"]) > 1:
            return redirect("core:pick_organisation")

        return redirect(getattr(settings, "LOGIN_REDIRECT_URL", "/"))
