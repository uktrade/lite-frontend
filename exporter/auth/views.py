from urllib.parse import urljoin

from django.conf import settings
from django.http import HttpResponseServerError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic.base import View

from core.auth import views as auth_views
from core.auth.utils import get_client
from exporter.auth.services import authenticate_exporter_user
from lite_forms.generators import error_page
from exporter.organisation.members.services import get_user
from exporter.auth.utils import get_profile


class AuthCallbackView(auth_views.AbstractAuthCallbackView, View):
    @cached_property
    def user_profile(self):
        return get_profile(get_client(self.request))

    def authenticate_user(self):
        return authenticate_exporter_user(self.request, self.user_profile)

    def handle_failure(self, data, status_code):
        if status_code == 400:
            return error_page(self.request, data["errors"][0])
        elif status_code == 401:
            return redirect("core:register_an_organisation_triage")

    def handle_success(self, data, status_code):
        self.request.session["first_name"] = data["first_name"]
        self.request.session["last_name"] = data["last_name"]
        self.request.session["user_token"] = data["token"]
        self.request.session["lite_api_user_id"] = data["lite_api_user_id"]
        return redirect(self.get_success_url())

    def get_success_url(self):
        user = get_user(self.request)
        if not user["organisations"]:
            return reverse("core:register_an_organisation_triage")
        elif len(user["organisations"]) == 1:
            organisation = user["organisations"][0]
            if organisation["status"]["key"] != "in_review":
                self.request.session["organisation"] = user["organisations"][0]["id"]
            else:
                return reverse("core:register_an_organisation_confirm")
        elif len(user["organisations"]) > 1:
            return reverse("core:pick_organisation")
        return settings.LOGIN_REDIRECT_URL
