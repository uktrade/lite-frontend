from http import HTTPStatus
import rules

from collections import OrderedDict
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, View, FormView
from django.contrib.auth.mixins import UserPassesTestMixin

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status
from core.helpers import stream_document_response
from core.services import stream_document

from caseworker.activities.forms import NotesAndTimelineForm
from caseworker.activities.mixins import NotesAndTimelineMixin
from caseworker.advice.services import move_case_forward
from caseworker.cases.forms.queries import CloseQueryForm
from caseworker.cases.helpers.case import CaseworkerMixin
from caseworker.cases.helpers.ecju_queries import get_ecju_queries
from caseworker.cases.services import get_case, post_ecju_query, get_application_documents, get_case_documents
from caseworker.f680.forms import NewECJUQueryForm
from caseworker.cases.views.queries import CloseQueryMixin
from caseworker.core.constants import ALL_CASES_QUEUE_ID
from caseworker.core.services import get_denial_reasons, get_permissible_statuses, group_denial_reasons
from caseworker.f680.recommendation.services import get_pending_recommendation_requests
from caseworker.picklists.services import get_picklists_list
from caseworker.queues.services import get_queue
from caseworker.users.services import get_gov_user


class F680CaseworkerMixin(UserPassesTestMixin, CaseworkerMixin):
    current_tab = None

    def test_func(self):
        return rules.test_rule("can_user_modify_f680", self.request)

    def handle_no_permission(self):
        raise PermissionDenied("Cannot modify or view F680s")

    def dispatch(self, request, *args, **kwargs):
        self.extra_setup(request)
        return super().dispatch(request, *args, **kwargs)

    def extra_setup(self, request):
        self.case_id = str(self.kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = self.kwargs["queue_pk"]
        self.queue = get_queue(request, self.queue_id)
        self.caseworker_id = str(self.request.session["lite_api_user_id"])
        data, _ = get_gov_user(self.request, self.caseworker_id)
        self.caseworker = data["user"]
        self.security_release_requests = OrderedDict()
        for rr in self.case["data"]["security_release_requests"]:
            self.security_release_requests[rr["id"]] = rr

        self.conditions = get_picklists_list(request, type="proviso", disable_pagination=True, show_deactivated=False)
        self.refusal_reasons = get_denial_reasons(request)
        self.denial_reasons_choices = group_denial_reasons(self.refusal_reasons)
        self.pending_recommendations = get_pending_recommendation_requests(self.request, self.case, self.caseworker)

    def pending_recommendation_requests(self):
        return get_pending_recommendation_requests(self.request, self.case, self.caseworker)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["case"] = self.case
        context_data["queue_id"] = self.queue_id
        context_data["current_tab"] = self.current_tab
        context_data["queue_pk"] = self.queue_id
        context_data["caseworker"] = self.caseworker
        context_data["security_release_requests"] = list(self.security_release_requests.values())
        submitted_by = self.case["data"]["submitted_by"]
        if submitted_by and "first_name" in submitted_by:
            self.case["data"]["submitted_by"] = " ".join([submitted_by["first_name"], submitted_by["last_name"]])

        # TODO: LTD-6075 - Implement a pattern for casetype-agnostic feature URLs
        # This flag is used to select the relevant f680 url(s) within shared templates.
        # Once LTD-6075 is implemented this should no longer be required.
        context_data["is_f680"] = True
        return context_data


class CaseDetailView(LoginRequiredMixin, F680CaseworkerMixin, TemplateView):
    template_name = "f680/case/detail.html"
    current_tab = "application-details"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        application_section_order = [
            "general_application_details",
            "approval_type",
            "product_information",
            "user_information",
            "supporting_documents",
            "notes_for_case_officers",
        ]
        application_sections = {
            key: self.case["data"]["application"]["sections"].get(key, None) for key in application_section_order
        }
        context_data["application_sections"] = application_sections
        context_data["permissible_statuses"] = get_permissible_statuses(self.request, self.case)
        return context_data


class CaseSummaryView(LoginRequiredMixin, F680CaseworkerMixin, TemplateView):
    template_name = "f680/case/summary.html"
    current_tab = "application-summary"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["permissible_statuses"] = get_permissible_statuses(self.request, self.case)
        return context


class MoveCaseForward(LoginRequiredMixin, F680CaseworkerMixin, View):

    def test_func(self):
        return all([super().test_func(), rules.test_rule("can_user_move_case_forward", self.request, self.case)])

    def handle_no_permission(self):
        raise PermissionDenied("Cannot move case forward")

    def post(self, request, **kwargs):
        move_case_forward(request, self.case_id, str(self.queue_id))

        all_cases_queue_url = reverse("cases:f680:details", kwargs={"queue_pk": ALL_CASES_QUEUE_ID, "pk": self.case_id})
        # WARNING: When changing this message be aware that the content is marked
        #   as safe. No user-supplied string should be injected in to it
        success_message = mark_safe(  # noqa: S308
            f"<a href='{all_cases_queue_url}' class='govuk-link govuk-link--inverse'>{self.case.reference_code}</a>&nbsp;"
            "was successfully moved forward"
        )
        messages.success(self.request, success_message, extra_tags="safe")
        queue_url = reverse("queues:cases", kwargs={"queue_pk": self.queue_id})
        return redirect(queue_url)


class NotesAndTimelineView(LoginRequiredMixin, F680CaseworkerMixin, NotesAndTimelineMixin, FormView):
    template_name = "f680/case/notes-and-timeline.html"
    current_tab = "notes-and-timeline"
    form_class = NotesAndTimelineForm

    def get_view_url(self):
        return reverse("cases:f680:notes_and_timeline", kwargs={"pk": self.case_id, "queue_pk": self.queue_id})


class ECJUQueryListView(LoginRequiredMixin, F680CaseworkerMixin, TemplateView):
    template_name = "f680/case/queries/list.html"
    current_tab = "ecju-queries"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        open_ecju_queries, closed_ecju_queries = get_ecju_queries(self.request, self.case_id)
        open_ecju_queries_with_forms = self.get_open_ecju_queries_with_forms(open_ecju_queries)
        context["open_queries"] = open_ecju_queries_with_forms
        context["closed_queries"] = closed_ecju_queries
        return context

    def get_open_ecju_queries_with_forms(self, open_ecju_queries):
        open_ecju_queries_with_forms = []
        for open_query in open_ecju_queries:
            open_ecju_queries_with_forms.append((open_query, CloseQueryForm(prefix=str(open_query["id"]))))
        return open_ecju_queries_with_forms


class NewECJUQueryView(LoginRequiredMixin, F680CaseworkerMixin, FormView):
    template_name = "f680/case/queries/new.html"
    form_class = NewECJUQueryForm

    def test_func(self):
        return all([super().test_func(), rules.test_rule("can_user_add_an_ecju_query", self.request, self.case)])

    def handle_no_permission(self):
        raise PermissionDenied("Cannot add ecju query to F680")

    def form_valid(self, form):
        data = {"question": form.cleaned_data["question"], "query_type": "ecju_query"}
        post_ecju_query(self.request, self.case_id, data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:f680:ecju_queries", kwargs={"pk": self.case_id, "queue_pk": self.queue_id})


class CloseECJUQueryView(LoginRequiredMixin, F680CaseworkerMixin, CloseQueryMixin, FormView):
    form_class = CloseQueryForm
    template_name = "f680/case/queries/close.html"

    def test_func(self):
        return all([super().test_func(), rules.test_rule("can_user_add_an_ecju_query", self.request, self.case)])

    def get_success_url(self):
        return reverse("cases:f680:ecju_queries", kwargs={"pk": self.case_id, "queue_pk": self.queue_id})


class SupportingDocumentsView(LoginRequiredMixin, F680CaseworkerMixin, TemplateView):
    template_name = "f680/case/supporting_documents.html"
    current_tab = "supporting-documents"

    @expect_status(
        HTTPStatus.OK,
        "Error retreiving uploaded supporting documents",
        "Unexpected error retreiving uploaded supporting documents",
    )
    def get_exporter_uploaded_supporting_documents(self):
        return get_application_documents(self.request, self.case_id)

    @expect_status(
        HTTPStatus.OK,
        "Error retreiving generated documents",
        "Unexpected error retreiving generated documents",
    )
    def get_caseworker_generated_documents(self):
        return get_case_documents(self.request, self.case_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uploaded_documents, _ = self.get_exporter_uploaded_supporting_documents()
        generated_documents, _ = self.get_caseworker_generated_documents()
        documents = uploaded_documents["results"] + generated_documents["documents"]
        context["supporting_documents"] = documents
        return context


class SupportingDocumentStreamView(LoginRequiredMixin, F680CaseworkerMixin, View):
    @expect_status(
        HTTPStatus.OK,
        "Error downloading document",
        "Unexpected error downloading document",
    )
    def stream_document(self, request, pk):
        return stream_document(request, pk=pk)

    def get(self, request, **kwargs):
        api_response, _ = self.stream_document(request, pk=kwargs["file_pk"])
        return stream_document_response(api_response)
