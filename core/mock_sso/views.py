import uuid

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    FormView,
    View,
)
from django.views.generic import RedirectView

from requests.models import PreparedRequest

from .forms import LoginForm


MOCK_SSO_ACCESS_TOKEN_CACHE_KEY = "MOCK_SSO_ACCESS_TOKEN_CACHE_KEY"  # nosec B105
MOCK_SSO_EMAIL_CACHE_KEY = "MOCK_SSO_EMAIL_CACHE_KEY"
MOCK_SSO_EMAIL_SESSION_KEY = "MOCK_SSO_EMAIL_SESSION_KEY"


def get_email_cache_key_from_code(code):
    return f"{MOCK_SSO_EMAIL_CACHE_KEY}-code-{code}"


def get_email_cache_key_from_access_token(access_token):
    return f"{MOCK_SSO_ACCESS_TOKEN_CACHE_KEY}-access-token-{access_token}"


# The mock sso here implements a barebones OAuth flow.
#
# The Authorize endpoint will return an access code which can then be used to
# retrieve an access token from the Token endpoint.
# The Token endpoint will then return an access token that can be used in
# requests to the APIUserMe to get details about the user.
#
# In the Authorize endpoint we work out the user that we want to login in.
# This is provided either by being explicitly set in settings or by displaying
# a login form.
# We then store this email in the cache paired with the access code.
#
# When the access code is then swapped for an access token we can retrieve the
# paired email address from the cache and then generate an access token paired
# to the same email address.
#
# This access token can then be used to retrieve details about the user and it
# will return the same email address that was set in the initial Authorize call.
#
# This is copying exactly how an OAuth flow would work for real without any real
# authorisation and most importantly allows us to login as any user by supplying
# the email address via a login prompt displayed when a user tries to login.
#
# NOTE: THIS IS ONLY FOR LOCAL DEVELOPMENT AND TESTING PURPOSES.


class Authorize(FormView):
    form_class = LoginForm
    template_name = "core/form.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.GET.get("state"):
            return HttpResponseBadRequest("state GET parameter is required")
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_uri(self, code):
        redirect_uri_base = self.request.GET.get("redirect_uri")
        req = PreparedRequest()
        params = {"code": code, "state": self.request.GET.get("state")}
        req.prepare_url(redirect_uri_base, params)
        return req.url

    def redirect_to_redirect_uri(self, request, email):
        # An access code is generated and sent back as part of the OAuth flow.
        # We store this in cache so that future requests to the token endpoint
        # can respond with an access token that corresponds to this stored
        # email.
        code = str(uuid.uuid4())
        cache.set(get_email_cache_key_from_code(code), email)

        # We store the email in session so that we can skip the login prompt in
        # future requests.
        request.session[MOCK_SSO_EMAIL_SESSION_KEY] = email

        return redirect(self.get_redirect_uri(code))

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        return self.redirect_to_redirect_uri(self.request, email)

    def get(self, request, *args, **kwargs):
        # Once a user has logged in via the mock sso once we will have put their
        # email into session so they don't need to fill in the email again.
        # In this case we can just skip the login prompt and redirect back.
        session_user_email = request.session.get(MOCK_SSO_EMAIL_SESSION_KEY)
        if session_user_email:
            return self.redirect_to_redirect_uri(request, session_user_email)

        # If we have an explicit email set in settings then we don't need to
        # show the mock sso login prompt so we can just redirect back.

        mock_sso_user_email = getattr(settings, "MOCK_SSO_USER_EMAIL", None)
        if mock_sso_user_email:
            return self.redirect_to_redirect_uri(request, mock_sso_user_email)

        return super().get(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class Token(View):
    def post(self, request, **kwargs):
        # We use the code to get the email address out of the cache that we
        # stored in the Authorize call.
        email = cache.get(get_email_cache_key_from_code(request.POST["code"]))

        # Then we respond back with an access token that also pairs up with
        # this email address, which itself is stored in the cache.
        # This means that future calls to the APIUserMe endpoint will respond
        # with the correct email address.
        access_token = str(uuid.uuid4())
        cache.set(get_email_cache_key_from_access_token(access_token), email)

        return JsonResponse(
            {
                "access_token": access_token,
                "token_type": "Bearer",
                "id_token": "DUMMYIDTOKEN",
            }
        )


class APIUserMe(View):
    def get(self, request, **kwargs):
        # We use the access token sent back from the Token endpoint to retrieve
        # the email that was originally sent as part of the Authorize flow.
        _, access_token = request.headers["Authorization"].split(" ")
        email = cache.get(get_email_cache_key_from_access_token(access_token))

        response_data = {
            "email": email,
            "contact_email": email,
            "email_user_id": email,
            "user_id": "20a0353f-a7d1-4851-9af8-1bcaff152b60",
            "first_name": settings.MOCK_SSO_USER_FIRST_NAME,
            "last_name": settings.MOCK_SSO_USER_LAST_NAME,
            "related_emails": [],
            "groups": [],
            "permitted_applications": [],
            "access_profiles": [],
        }
        return JsonResponse(response_data)


class Logout(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        redirect_url = self.request.build_absolute_uri("/")
        self.request.session.flush()
        return redirect_url
