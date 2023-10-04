from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from requests.models import PreparedRequest


class Authorize(View):
    def get(self, request, **kwargs):
        if not request.GET.get("state"):
            return HttpResponseBadRequest("state GET parameter is required")
        redirect_uri_base = request.GET.get("redirect_uri")
        req = PreparedRequest()
        params = {"code": "DUMMYCODE", "state": request.GET.get("state")}
        req.prepare_url(redirect_uri_base, params)
        redirect_uri = req.url
        return redirect(redirect_uri)


@method_decorator(csrf_exempt, name="dispatch")
class Token(View):
    def post(self, request, **kwargs):
        return JsonResponse({"access_token": "DUMMYTOKEN", "token_type": "Bearer"})


class APIUserMe(View):
    def get(self, request, **kwargs):
        response_data = {
            "email": settings.MOCK_SSO_USER_EMAIL,
            "contact_email": settings.MOCK_SSO_USER_EMAIL,
            "email_user_id": settings.MOCK_SSO_USER_EMAIL,
            "user_id": "20a0353f-a7d1-4851-9af8-1bcaff152b60",
            "first_name": settings.MOCK_SSO_USER_FIRST_NAME,
            "last_name": settings.MOCK_SSO_USER_LAST_NAME,
            "related_emails": [],
            "groups": [],
            "permitted_applications": [],
            "access_profiles": [],
        }
        return JsonResponse(response_data)
