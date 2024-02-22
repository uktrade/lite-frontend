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

from requests.models import PreparedRequest

from .forms import LoginForm


MOCK_SSO_ACCESS_TOKEN_CACHE_KEY = "MOCK_SSO_ACCESS_TOKEN_CACHE_KEY"  # nosec B105
MOCK_SSO_EMAIL_CACHE_KEY = "MOCK_SSO_EMAIL_CACHE_KEY"
MOCK_SSO_EMAIL_SESSION_KEY = "MOCK_SSO_EMAIL_SESSION_KEY"


def get_email_cache_key_from_code(code):
    return f"{MOCK_SSO_EMAIL_CACHE_KEY}-code-{code}"


def get_email_cache_key_from_access_token(access_token):
    return f"{MOCK_SSO_ACCESS_TOKEN_CACHE_KEY}-access-token-{access_token}"


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
        code = str(uuid.uuid4())
        cache.set(get_email_cache_key_from_code(code), email)
        request.session[MOCK_SSO_EMAIL_SESSION_KEY] = email
        return redirect(self.get_redirect_uri(code))

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        return self.redirect_to_redirect_uri(self.request, email)

    def get(self, request, *args, **kwargs):
        session_user_email = request.session.get(MOCK_SSO_EMAIL_SESSION_KEY)
        if session_user_email:
            return self.redirect_to_redirect_uri(request, session_user_email)

        mock_sso_user_email = getattr(settings, "MOCK_SSO_USER_EMAIL", None)
        if mock_sso_user_email:
            return self.redirect_to_redirect_uri(request, mock_sso_user_email)

        return super().get(request, *args, **kwargs)


@method_decorator(csrf_exempt, name="dispatch")
class Token(View):
    def post(self, request, **kwargs):
        email = cache.get(get_email_cache_key_from_code(request.POST["code"]))
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
