import base64
from http import HTTPStatus
import json

from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView
from django.http import Http404
from django.urls import reverse_lazy

from rest_framework.response import Response
from rest_framework import views

from caseworker.search.helpers import group_results_by_combination
from caseworker.search.services import get_product_autocomplete, get_product_search_results
from core.auth.views import LoginRequiredMixin

from caseworker.external_data import forms, services
from lite_forms.generators import error_page
from .forms import DenialSearchForm, DenialSearchSuggestForm

with open(settings.BASE_DIR + "/caseworker/external_data/example.csv", "rb") as f:
    base_64_csv = base64.b64encode(f.read()).decode()


class DenialUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "external_data/denial-upload.html"
    form_class = forms.DenialUploadForm
    success_message = "Denials created successfully"
    extra_context = {"base_64_csv": base_64_csv}

    def dispatch(self, request, *args, **kwargs):
        raise Http404("CSV denials uploads have been disabled")

    def form_valid(self, form):
        response = services.upload_denials(request=self.request, data=form.cleaned_data)
        if not response.ok:
            for key, errors in response.json()["errors"].items():
                for error in errors:
                    form.add_error(key, error)
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return self.request.get_full_path()


class DenialDetailView(LoginRequiredMixin, TemplateView):
    template_name = "external_data/denial-detail.html"

    def get_context_data(self, **kwargs):
        queue_id = self.request.GET.get("queue_id", None)
        case_id = self.request.GET.get("case_id", None)
        denial = services.get_denial(request=self.request, pk=self.kwargs["pk"])
        return super().get_context_data(denial=denial, queue_id=queue_id, case_id=case_id, **kwargs)


class DenialRevokeView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "external_data/denial-revoke.html"
    success_message = "Denial successfully revoked"
    form_class = forms.DenialRevoke

    def get_context_data(self, **kwargs):
        queue_id = self.request.GET.get("queue_id", None)
        case_id = self.request.GET.get("case_id", None)
        denial = services.get_denial(request=self.request, pk=self.kwargs["pk"])
        return super().get_context_data(denial=denial, queue_id=queue_id, case_id=case_id, **kwargs)

    def get_success_url(self):
        return reverse("external_data:denial-detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        services.revoke_denial(request=self.request, pk=self.kwargs["pk"], comment=form.cleaned_data["comment"])
        return super().form_valid(form)


class DenialSearchView(LoginRequiredMixin, FormView):
    form_class = DenialSearchForm
    template_name = "external_data/denial-search.html"
    success_url = reverse_lazy("external-data:denial-search")

    def get_initial(self):
        return {
            "search_string": self.request.GET.get("search_string", ""),
            "page": self.request.GET.get("page", 1),
        }

    def dispatch(self, request, *args, **kwargs):
        # when we first get to the page query_params are empty.
        # if we don't use empty string then search term becomes None
        # and we get some results even though the input field is empty
        query_params = {
            "search": self.request.GET.get("search_string", ""),
            "page": self.request.GET.get("page", 1),
        }

        self.results, status = services.get_denial_search_results(self.request, query_params)

        if status not in (HTTPStatus.OK, HTTPStatus.BAD_REQUEST):
            return error_page(self.request, getattr(self.results, "error", "An error occurred"))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_pages = 1
        form = self.get_form()
        if "errors" not in self.results.keys():
            self.results = group_results_by_combination(self.results)
            total_pages = self.results["count"] // form.page_size
        return {
            **context,
            "customiser_spec": self.customiser_spec(),
            "data": {"total_pages": total_pages},
            "search_results": self.results,
        }

    def customiser_spec(self) -> str:
        return json.dumps(
            {
                "options_label": "Customise search results",
                "identifier": "product-search-view",
                "analytics_prefix": "psv",
                "options_hint": "Select columns to show",
                "toggleable_elements": [
                    {"label": "Reference", "key": "reference", "default_visible": True},
                    {"label": "Regime Reference", "key": "regime_reference", "default_visible": True},
                    {"label": "Name", "key": "name", "default_visible": True},
                    {"label": "Regime", "key": "regime", "default_visible": True},
                    {"label": "Address", "key": "address", "default_visible": True},
                ],
            }
        )


class DenialSearchSuggestView(LoginRequiredMixin, views.APIView):
    def get(self, request):
        query = ""

        form = DenialSearchSuggestForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["q"]

        results = get_product_autocomplete(self.request, query)
        return Response(results)
