from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import FormView, TemplateView
from requests.exceptions import HTTPError


from caseworker.advice.constants import AdviceType
from core import client
from core.auth.views import LoginRequiredMixin

from caseworker.advice.services import post_bulk_approval_recommendation
from caseworker.advice.views.mixins import CaseContextMixin
from caseworker.advice.forms.bulk_approval import RecommendBulkApprovalForm
from caseworker.cases.services import get_case_basic_details
from caseworker.picklists.services import get_picklists_list
from caseworker.users.services import get_gov_user


class BulkApprovalView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """
    Form to recommend approval advice for all products on the application
    """

    template_name = "advice/bulk-approval.html"
    form_class = RecommendBulkApprovalForm

    @property
    def caseworker_id(self):
        return str(self.request.session["lite_api_user_id"])

    @property
    def caseworker(self):
        data, _ = get_gov_user(self.request, self.caseworker_id)
        return data["user"]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        approval_reason = get_picklists_list(
            self.request, type="standard_advice", disable_pagination=True, show_deactivated=False
        )
        proviso = get_picklists_list(self.request, type="proviso", disable_pagination=True, show_deactivated=False)

        footnote_details = get_picklists_list(
            self.request, type="footnotes", disable_pagination=True, show_deactivated=False
        )

        kwargs["approval_reason"] = approval_reason
        kwargs["proviso"] = proviso
        kwargs["footnote_details"] = footnote_details
        return kwargs

    def get_cases_data(self):
        case_ids = self.request.GET.getlist("cases", [])
        cases_data = [get_case_basic_details(self.request, case_id) for case_id in case_ids]
        return cases_data

    def form_valid(self, form):
        queue_id = self.kwargs["pk"]
        case_ids = self.request.GET.getlist("cases", [])
        advice_data = form.cleaned_data
        response, status_code = post_bulk_approval_recommendation(
            self.request, self.caseworker, queue_id, case_ids, advice_data
        )

        if status_code == 201:
            num_cases = len(response["case_ids"])
            messages.success(self.request, f"successfully approved {num_cases} case" + "s" if num_cases > 1 else "")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("queues:cases", kwargs={"queue_pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cases_data = self.get_cases_data()
        return {
            **context,
            "title": "Bulk approval",
            "cases_data": cases_data,
        }
