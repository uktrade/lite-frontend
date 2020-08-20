from abc import ABCMeta, abstractmethod

from django.conf import settings
from django.views.generic import RedirectView
from requests_oauthlib import OAuth2Session


class AuthView(RedirectView, metaclass=ABCMeta):
    """"
    Abstract base class for a 'redirect to sso' view

    Implement `get_client` to return an OAuth2Session
    and also set AUTHORIZATION_URL and TOKEN_SESSION_KEY
    in your subclass

    """

    permanent = False

    AUTHORIZATION_URL = None
    TOKEN_SESSION_KEY = None

    @abstractmethod
    def get_client(self) -> OAuth2Session:
        raise NotImplementedError()

    def get_redirect_url(self, *args, **kwargs):

        authorization_url, state = self.get_client().authorization_url(self.AUTHORIZATION_URL)

        self.request.session[self.TOKEN_SESSION_KEY + "_oauth_state"] = state

        return authorization_url


class AuthLogoutView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        self.request.session.flush()
        return settings.LOGOUT_URL + self.request.build_absolute_uri("/")
