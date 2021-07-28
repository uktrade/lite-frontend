import abc
from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseServerError, QueryDict
from django.shortcuts import redirect, resolve_url
from django.utils.functional import cached_property
from django.urls import reverse
from django.views.generic import RedirectView
from django.views.generic.base import View

from lite_content.lite_internal_frontend import strings
from lite_forms.generators import error_page

from caseworker.auth.services import authenticate_gov_user
from exporter.auth.services import authenticate_exporter_user
from caseworker.auth.helpers import save_internal_user_info_to_session, save_exporter_user_info_to_session

from core.auth.utils import get_profile


class AuthView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url, state = self.request.authbroker_client.authorization_url(settings.AUTHBROKER_AUTHORIZATION_URL)
        self.request.session[f"{settings.TOKEN_SESSION_KEY}_oauth_state"] = state
        return url


class AuthLogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        self.request.session.flush()
        return settings.LOGOUT_URL + self.request.build_absolute_uri("/")


class AbstractAuthCallbackView(abc.ABC, View):
    @abc.abstractmethod
    def handle_failure(self, data, status_code):
        pass

    @abc.abstractmethod
    def handle_success(self, data, status_code):
        pass

    @abc.abstractmethod
    def authenticate_user(self):
        pass

    @cached_property
    def user_profile(self):
        return get_profile(self.request.authbroker_client)

    def get(self, request, *args, **kwargs):
        auth_code = request.GET.get("code", None)
        if not auth_code:
            return redirect(reverse("auth:login"))
        state = self.request.session.get(f"{settings.TOKEN_SESSION_KEY}_oauth_state", None)
        if not state:
            return HttpResponseServerError()
        token = request.authbroker_client.fetch_token(
            settings.AUTHBROKER_TOKEN_URL, client_secret=settings.AUTHBROKER_CLIENT_SECRET, code=auth_code
        )
        self.request.session[settings.TOKEN_SESSION_KEY] = dict(token)
        del self.request.session[f"{settings.TOKEN_SESSION_KEY}_oauth_state"]
        data, status_code = self.authenticate_user()

        if status_code == 200:
            return self.handle_success(data=data, status_code=status_code)
        return self.handle_failure(data=data, status_code=status_code)


class LoginRequiredMixin:
    """
    Redirects to the appropriate login according to which service this repo is running as.
    """

    @property
    def user_profile(self):
        return get_profile(self.request.authbroker_client)

    def redirect_to_login(self):
        resolved_url = resolve_url(settings.LOGIN_URL)
        login_url_parts = list(urlparse(resolved_url))
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring["next"] = self.request.get_full_path()
        login_url_parts[4] = querystring.urlencode(safe="/")
        return HttpResponseRedirect(urlunparse(login_url_parts))

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

        if settings.SERVICE_NAME == "lite-internal-frontend":
            return self.auth_internal_user(self, *args, **kwargs)

        return super().dispatch(request, *args, **kwargs)
