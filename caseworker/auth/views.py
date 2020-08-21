from urllib.parse import urljoin

from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.views.generic.base import View

from caseworker.auth.services import authenticate_gov_user
from core.auth.utils import get_client
from django.conf import settings
from lite_content.lite_internal_frontend import strings
from lite_forms.generators import error_page
from core.auth import views as auth_views
from caseworker.auth.utils import get_profile


class AuthCallbackView(auth_views.AbstractAuthCallbackView, View):
    @cached_property
    def user_profile(self):
        return get_profile(get_client(self.request))

    def authenticate_user(self):
        return authenticate_gov_user(self.request, self.user_profile)

    def handle_success(self, data):
        self.request.session["first_name"] = self.profile["first_name"]
        self.request.session["last_name"] = self.profile["last_name"]
        self.request.session["default_queue"] = data["default_queue"]
        self.request.session["user_token"] = data["token"]
        self.request.session["lite_api_user_id"] = data["lite_api_user_id"]
        self.request.session.save()
        return redirect(settings.LOGIN_REDIRECT_URL)

    def handle_failure(self, data, status_code):
        return error_page(
            None,
            title=strings.Authentication.UserDoesNotExist.TITLE,
            description=strings.Authentication.UserDoesNotExist.DESCRIPTION,
            show_back_link=False,
        )
