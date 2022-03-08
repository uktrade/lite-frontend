from django.shortcuts import redirect
from django.views.generic.base import View

from caseworker.auth.services import authenticate_gov_user
from django.conf import settings
from lite_content.lite_internal_frontend import strings
from lite_forms.generators import error_page
from core.auth import views as auth_views


class AuthCallbackView(auth_views.AbstractAuthCallbackView, View):
    def authenticate_user(self):
        return authenticate_gov_user(self.request, self.user_profile)

    def handle_success(self, data, status_code):
        self.request.session["first_name"] = self.user_profile["first_name"]
        self.request.session["last_name"] = self.user_profile["last_name"]
        self.request.session["default_queue"] = data["default_queue"]
        self.request.session["user_token"] = data["token"]
        self.request.session["lite_api_user_id"] = data["lite_api_user_id"]
        self.request.session["email"] = self.user_profile["email"]
        self.request.session.save()
        return redirect(settings.LOGIN_REDIRECT_URL)

    def handle_failure(self, data, status_code):
        return error_page(
            None,
            title=strings.Authentication.UserDoesNotExist.TITLE,
            description=strings.Authentication.UserDoesNotExist.DESCRIPTION,
            show_back_link=False,
        )

    def fetch_token(self, request, auth_code):
        return request.authbroker_client.fetch_token(
            settings.AUTHBROKER_TOKEN_URL, client_secret=settings.AUTHBROKER_CLIENT_SECRET, code=auth_code
        )
