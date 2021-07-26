from django.shortcuts import redirect
from django.views.generic.base import View

from django.conf import settings

from caseworker.auth.services import authenticate_gov_user
from caseworker.auth.helpers import save_internal_user_info_to_session

from lite_content.lite_internal_frontend import strings
from lite_forms.generators import error_page

from core.auth import views as auth_views


class AuthCallbackView(auth_views.AbstractAuthCallbackView, View):
    def authenticate_user(self):
        return authenticate_gov_user(self.request, self.user_profile)

    def handle_success(self, data, status_code):
        save_internal_user_info_to_session(self.request.session, data, self.user_profile)
        return redirect(settings.LOGIN_REDIRECT_URL)

    def handle_failure(self, data, status_code):
        return error_page(
            None,
            title=strings.Authentication.UserDoesNotExist.TITLE,
            description=strings.Authentication.UserDoesNotExist.DESCRIPTION,
            show_back_link=False,
        )
