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


class CaseworkerLoginRequiredMixin(auth_views.LoginRequiredMixin):
    def auth_internal_user(self, *args, **kwargs):
        data, status_code = authenticate_gov_user(self.request, self.user_profile)

        if status_code == 403:
            return error_page(
                self.request,
                title=strings.Authentication.UserDoesNotExist.TITLE,
                description=strings.Authentication.UserDoesNotExist.DESCRIPTION,
                show_back_link=False,
            )

        elif status_code != 200:
            return error_page(self.request, show_back_link=False)

        # success
        save_internal_user_info_to_session(self.request.session, data, self.user_profile)
        return super().dispatch(self.request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        # is user logged in to SSO?
        if not self.request.authbroker_client.authorized:
            return self.redirect_to_login()

        return self.auth_internal_user(self, *args, **kwargs)
