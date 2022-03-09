import abc
from urllib.parse import urlparse, urlunparse

from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseServerError, QueryDict
from django.shortcuts import redirect, resolve_url
from django.utils.functional import cached_property
from django.urls import reverse
from django.views.generic import RedirectView
from django.views.generic.base import View

from core.auth.utils import get_profile
import uuid


class AuthView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url, state = self.request.authbroker_client.create_authorization_url(
            settings.AUTHBROKER_AUTHORIZATION_URL, nonce=uuid.uuid4().hex
        )
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

    @abc.abstractmethod
    def fetch_token(self, request, auth_code):
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

        token = self.fetch_token(request, auth_code)
        self.request.session[settings.TOKEN_SESSION_KEY] = dict(token)
        del self.request.session[f"{settings.TOKEN_SESSION_KEY}_oauth_state"]
        data, status_code = self.authenticate_user()

        if status_code == 200:
            return self.handle_success(data=data, status_code=status_code)
        return self.handle_failure(data=data, status_code=status_code)


class LoginRequiredMixin:
    def redirect_to_login(self):
        resolved_url = resolve_url(settings.LOGIN_URL)
        login_url_parts = list(urlparse(resolved_url))
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring["next"] = self.request.get_full_path()
        login_url_parts[4] = querystring.urlencode(safe="/")
        return HttpResponseRedirect(urlunparse(login_url_parts))

    def dispatch(self, request, *args, **kwargs):
        if not self.request.authbroker_client.token:
            return self.redirect_to_login()
        return super().dispatch(request, *args, **kwargs)
