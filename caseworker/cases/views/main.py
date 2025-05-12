import rules

from dateutil.parser import parse
from decimal import Decimal
from logging import getLogger
from http import HTTPStatus

from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import (
    redirect,
)
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.functional import cached_property
from django.views.generic import (
    FormView,
    TemplateView,
    View,
)

from requests.exceptions import HTTPError

from core.auth.views import LoginRequiredMixin
from core.builtins.custom_tags import filter_advice_by_level
from core.constants import (
    CaseStatusEnum,
    LicenceStatusEnum,
    SecurityClassifiedApprovalsType,
)
from core.decorators import expect_status
from core.exceptions import APIError
from core.helpers import (
    get_document_data,
    stream_document_response,
)
from core.services import stream_document
from lite_content.lite_internal_frontend import cases
from lite_content.lite_internal_frontend.cases import (
    ApplicationPage,
    CasePage,
    DoneWithCaseOnQueueForm,
    Manage,
)

from lite_forms.generators import error_page, form_page
from lite_forms.helpers import conditional
from lite_forms.views import SingleFormView

from caseworker.advice.services import get_advice_tab_context
from caseworker.cases.forms.attach_documents import attach_documents_form
from caseworker.cases.forms.change_status import ChangeStatusForm
from caseworker.cases.forms.change_sub_status import ChangeSubStatusForm
from caseworker.cases.forms.change_licence_status import (
    ChangeLicenceStatusConfirmationForm,
    ChangeLicenceStatusForm,
)
from caseworker.cases.forms.done_with_case import done_with_case_form
from caseworker.cases.forms.move_case import move_case_form
from caseworker.cases.forms.queries import CloseQueryForm
from caseworker.cases.forms.reissue_ogl_form import reissue_ogl_confirmation_form
from caseworker.cases.forms.rerun_routing_rules import rerun_routing_rules_confirmation_form
import caseworker.cases.helpers.advice as advice_helpers
from caseworker.cases.helpers.case import (
    CaseworkerMixin,
    LU_POST_CIRC_FINALISE_QUEUE_ALIAS,
    Slices,
    Tabs,
)
from caseworker.cases.helpers.ecju_queries import get_ecju_queries
from caseworker.cases.helpers.licence import get_latest_licence_status
from caseworker.cases.services import (
    get_case,
    post_case_notes,
    put_case_queues,
    put_unassign_queues,
    put_rerun_case_routing_rules,
    post_application_status,
    reissue_ogl,
    post_case_documents,
    get_blocking_flags,
    get_case_sub_statuses,
    put_case_sub_status,
    get_licence_details,
    update_licence_details,
    get_case_documents,
    get_case_additional_contacts,
    get_activity_filters,
    get_case_basic_details,
    get_user_case_queues,
)
from caseworker.core.constants import GENERATED_DOCUMENT
from caseworker.core.helpers import generate_activity_filters
from caseworker.core.objects import Tab
from caseworker.core.services import (
    get_permissible_statuses,
    get_status_properties,
    get_user_permissions,
)
from caseworker.core.constants import Permission
from caseworker.queues.services import get_queue
from caseworker.tau.utils import get_tau_tab_url_name
from caseworker.teams.services import get_teams
from caseworker.users.services import (
    get_gov_user,
)

logger = getLogger(__name__)


class CaseContextBasicMixin:
    """Most views need a reference to the associated Case details.
    These are mainly reference code and organisation to format page title.
    """

    @property
    def case_id(self):
        return str(self.request.GET.get("cases"))

    @cached_property
    def case(self):
        return get_case_basic_details(self.request, self.case_id)


class CaseTabsMixin:
    def get_tabs(self):
        tabs = [
            Tabs.QUICK_SUMMARY,
            Tabs.DETAILS,
            Tabs.LICENCES,
            Tabs.ECJU_QUERIES,
            Tabs.DOCUMENTS,
            self.get_notes_and_timelines_tab(),
            self.get_assessment_tab(),
            self.get_advice_tab(),
        ]

        return tabs

    def get_advice_tab(self):
        data, _ = get_gov_user(self.request, str(self.request.session["lite_api_user_id"]))
        return Tab(
            "advice",
            "Recommendations and decision",
            get_advice_tab_context(self.case, data["user"], str(self.kwargs["queue_pk"]))["url"],
            has_template=False,
        )

    def get_assessment_tab(self):
        return Tab(
            "assessment",
            "Product assessment",
            get_tau_tab_url_name(),
            has_template=False,
        )

    def get_notes_and_timelines_tab(self):
        return Tab(
            "activities",
            CasePage.Tabs.CASE_NOTES_AND_TIMELINE,
            "cases:activities:notes-and-timeline",
            has_template=False,
        )


class CaseDetail(CaseTabsMixin, CaseworkerMixin, TemplateView):
    template_name = "case/case.html"

    def get_advice_additional_context(self):
        status_props, _ = get_status_properties(self.request, self.case.data["status"]["key"])
        current_advice_level = ["user"]
        blocking_flags = get_blocking_flags(self.request, self.case["id"])

        if (
            filter_advice_by_level(self.case["advice"], "team")
            and Permission.MANAGE_TEAM_ADVICE.value in self.permissions
        ):
            current_advice_level += ["team"]

        final_advice = filter_advice_by_level(self.case["advice"], "final")

        if final_advice and advice_helpers.check_user_permitted_to_give_final_advice(self.permissions):
            current_advice_level += ["final"]

        if (
            not advice_helpers.can_user_create_and_edit_advice(self.case, self.permissions)
            or status_props["is_terminal"]
        ):
            current_advice_level = []

        final_goods_advice = advice_helpers.filter_advice_by_target(final_advice, "good")
        other_advice = [a for a in final_advice if a not in final_goods_advice]

        # approve/refuse on same product = cannot finalise
        # approve refuse NLR on different products in same application = can still finalise
        # no approvals or NLR on any goods = cannot finalise

        conflicting_goods_advice = advice_helpers.case_goods_has_conflicting_advice(self.case.goods, final_goods_advice)
        goods_can_finalise = advice_helpers.goods_can_finalise(self.case.goods, final_goods_advice)

        advice_types = set([f["type"]["key"] for f in other_advice])

        if advice_types == {"approve", "proviso"}:
            conflicting_other_advice = False
        else:
            conflicting_other_advice = len(advice_types) > 1

        conflicting_advice = conflicting_goods_advice or conflicting_other_advice

        if blocking_flags:
            logger.debug("Cannot finalise because of blocking_flags: %s", blocking_flags)
            return {
                "conflicting_advice": conflicting_advice,
                "teams": get_teams(self.request),
                "current_advice_level": current_advice_level,
                "can_finalise": False,
                "blocking_flags": blocking_flags,
            }

        refuse_all = set([f["type"]["key"] for f in final_advice]) == {"refuse"}

        can_finalise = (
            "final" in current_advice_level
            and advice_helpers.can_advice_be_finalised(self.case)
            and not conflicting_advice
            and goods_can_finalise
        ) or refuse_all

        return {
            "conflicting_advice": conflicting_advice,
            "teams": get_teams(self.request),
            "current_advice_level": current_advice_level,
            "can_finalise": can_finalise,
            "blocking_flags": blocking_flags,
        }

    def is_only_on_post_circ_queue(self):
        queue_alias = tuple(queue.get("alias") for queue in self.case.queue_details)
        return self.is_lu_user() and queue_alias == (LU_POST_CIRC_FINALISE_QUEUE_ALIAS,)

    def get_goods_summary(self):
        goods_summary = {
            "names": list(),
            "cles": set(),
            "regimes": set(),
            "report_summaries": set(),
            "total_value": 0,
        }
        for good in self.case.goods:
            goods_summary["cles"].update(list(cle["rating"] for cle in good["control_list_entries"]))
            goods_summary["regimes"].update(list(regime["name"] for regime in good["regime_entries"]))
            goods_summary["names"].append(good["good"]["name"])
            if "report_summary_subject" in good and good["report_summary_subject"]:
                report_summary = good["report_summary_subject"]["name"]
                if "report_summary_prefix" in good and good["report_summary_prefix"]:
                    report_summary = f"{good['report_summary_prefix']['name']} {report_summary}"
                goods_summary["report_summaries"].add(report_summary)
            # support legacy report_summary field until it is removed
            elif good.get("report_summary"):
                goods_summary["report_summaries"].add(good["report_summary"])

            goods_summary["total_value"] += Decimal(good["value"])
        return goods_summary

    def get_destination_countries(self):
        destination_countries = set()
        all_parties = self.case.data.get("ultimate_end_users", []) + self.case.data.get("third_parties", [])
        if self.case.data.get("end_user"):
            all_parties.append(self.case.data["end_user"])
        if self.case.data.get("consignee"):
            all_parties.append(self.case.data["consignee"])
        for party in all_parties:
            destination_countries.add(party["country"]["name"])
        return destination_countries

    def get_open_ecju_queries_with_forms(self, open_ecju_queries):
        open_ecju_queries_with_forms = []
        for open_query in open_ecju_queries:
            open_ecju_queries_with_forms.append((open_query, CloseQueryForm(prefix=str(open_query["id"]))))
        return open_ecju_queries_with_forms

    def get_context_data(self, *args, **kwargs):
        open_ecju_queries, closed_ecju_queries = get_ecju_queries(self.request, self.case_id)
        open_ecju_queries_with_forms = self.get_open_ecju_queries_with_forms(open_ecju_queries)
        user_assigned_queues = get_user_case_queues(self.request, self.case_id)[0]
        status_props, _ = get_status_properties(self.request, self.case.data["status"]["key"])
        can_set_done = (
            status_props["is_terminal"]
            and self.case.data["status"]["key"] != CaseStatusEnum.APPLICANT_EDITING
            and not self.is_tau_user()
        )

        context = super().get_context_data(*args, **kwargs)
        default_tab = "quick-summary"
        current_tab = default_tab if self.kwargs["tab"] == "default" else self.kwargs["tab"]
        show_actions_column = False
        for licence in self.case.licences:
            if rules.test_rule("can_licence_status_be_changed", self.request, licence):
                show_actions_column = True
                break

        return {
            **context,
            "tabs": self.tabs if self.tabs else self.get_tabs(),
            "current_tab": current_tab,
            "slices": [Slices.SUMMARY, *self.slices],
            "case": self.case,
            "queue": self.queue,
            "is_system_queue": self.queue["is_system_queue"],
            "goods_summary": self.get_goods_summary(),
            "destination_countries": self.get_destination_countries(),
            "user_assigned_queues": user_assigned_queues,
            "case_documents": get_case_documents(self.request, self.case_id)[0]["documents"],
            "open_queries": open_ecju_queries_with_forms,
            "closed_queries": closed_ecju_queries,
            "additional_contacts": get_case_additional_contacts(self.request, self.case_id),
            "permissions": self.permissions,
            "is_tau_user": self.is_tau_user(),
            "hide_im_done": self.is_tau_user() or self.is_only_on_post_circ_queue(),
            "can_set_done": can_set_done
            and (self.queue["is_system_queue"] and user_assigned_queues)
            or not self.queue["is_system_queue"],
            "generated_document_key": GENERATED_DOCUMENT,
            "permissible_statuses": get_permissible_statuses(self.request, self.case),
            "filters": generate_activity_filters(get_activity_filters(self.request, self.case_id), ApplicationPage),
            "is_terminal": status_props["is_terminal"],
            "security_classified_approvals_types": SecurityClassifiedApprovalsType,
            "user": self.caseworker,
            "show_actions_column": show_actions_column,
            "licence_status": get_latest_licence_status(self.case),
            **self.additional_context,
        }

    def _transform_data(self):
        self.case.total_days_elapsed = (timezone.now() - parse(self.case.submitted_at)).days
        if self.case.queue_details:
            for queue_detail in self.case.queue_details:
                queue_detail["days_on_queue_elapsed"] = (timezone.now() - parse(queue_detail["joined_queue_at"])).days

    def get_slices(self):
        return [
            Slices.GOODS,
            Slices.DESTINATIONS,
            conditional(self.case.data["denial_matches"], Slices.DENIAL_MATCHES),
            conditional(self.case.data["sanction_matches"], Slices.SANCTION_MATCHES),
            conditional(self.case.data["end_user"], Slices.END_USER_DOCUMENTS),
            conditional(self.case.data["inactive_parties"], Slices.DELETED_ENTITIES),
            Slices.LOCATIONS,
            Slices.SECURITY_APPROVALS,
            Slices.END_USE_DETAILS,
            Slices.SUPPORTING_DOCUMENTS,
            Slices.FREEDOM_OF_INFORMATION,
            conditional(self.case.data["appeal"], Slices.APPEAL_DETAILS),
        ]

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.case_id = str(kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = kwargs["queue_pk"]
        self.queue = get_queue(request, self.queue_id)
        self.permissions = get_user_permissions(self.request)

        self._transform_data()

        self.tabs = self.get_tabs()
        self.slices = self.get_slices()
        self.additional_context = self.get_advice_additional_context()


class CaseNotes(TemplateView):
    def post(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        response, status_code = post_case_notes(request, case_id, request.POST)

        if status_code != 201:
            return error_page(request, response.get("errors")["text"][0])

        queue_id = kwargs["queue_pk"]

        return redirect(
            "cases:activities:notes-and-timeline",
            pk=case_id,
            queue_pk=queue_id,
        )


class ImDoneView(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.data = {"queues": [str(kwargs["queue_pk"])]}
        self.context = {"case": case}
        self.form = done_with_case_form(request, kwargs["queue_pk"], self.object_pk)
        self.action = put_unassign_queues
        self.success_url = reverse_lazy("queues:cases", kwargs={"queue_pk": kwargs["queue_pk"]})
        self.success_message = DoneWithCaseOnQueueForm.SUCCESS_MESSAGE.format(case.reference_code)


class ChangeStatus(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ChangeStatusForm
    template_name = "case/form.html"
    success_message = "Case status successfully changed"

    def dispatch(self, *args, **kwargs):
        try:
            self.case = get_case(self.request, self.kwargs["pk"])
        except HTTPError:
            raise Http404()

        if not rules.test_rule("can_user_change_case", self.request, self.case):
            raise Http404()

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["case"] = self.case
        context["back_url"] = self.get_success_url()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        statuses = get_permissible_statuses(self.request, self.case)
        status_choices = [(status["key"], status["value"]) for status in statuses]
        kwargs["statuses"] = status_choices
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        status = self.case["data"].get("status")
        if status:
            initial["status"] = status["key"]
        return initial

    @expect_status(
        HTTPStatus.OK,
        "Error changing case status",
        "Unexpected error changing case status",
    )
    def change_case_status(self, request, case_id, data):
        return post_application_status(request, case_id, data)

    def form_valid(self, form):
        self.change_case_status(self.request, self.case.id, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return self.case.manifest.urls.get_detail_view_url(case_id=self.case.id, queue_pk=self.kwargs["queue_pk"])


class ChangeSubStatus(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ChangeSubStatusForm
    template_name = "case/form.html"
    success_message = "Case sub-status successfully changed"

    def dispatch(self, *args, **kwargs):
        try:
            self.case = get_case(self.request, self.kwargs["pk"])
        except HTTPError:
            raise Http404()

        if not rules.test_rule("can_user_change_sub_status", self.request, self.case):
            raise Http404()

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["case"] = self.case

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        case_sub_statuses = get_case_sub_statuses(self.request, self.case.id)
        case_sub_status_choices = [
            (case_sub_status["id"], case_sub_status["name"]) for case_sub_status in case_sub_statuses
        ]
        kwargs["sub_statuses"] = case_sub_status_choices

        return kwargs

    def get_initial(self):
        initial = super().get_initial()

        sub_status = self.case["data"].get("sub_status")
        if sub_status:
            initial["sub_status"] = sub_status["id"]

        return initial

    @expect_status(
        HTTPStatus.OK,
        "Error changing case sub-status",
        "Unexpected error changing case sub-status",
    )
    def put_case_sub_status(self, request, case_id, data):
        return put_case_sub_status(request, case_id, data)

    def form_valid(self, form):
        self.put_case_sub_status(
            self.request,
            self.case.id,
            form.cleaned_data,
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "cases:case",
            kwargs={
                "queue_pk": self.kwargs["queue_pk"],
                "pk": self.case.id,
                "tab": "details",
            },
        )


class BaseChangeLicenceStatus(LoginRequiredMixin, FormView):
    def dispatch(self, *args, **kwargs):
        try:
            self.licence = get_licence_details(self.request, self.kwargs["licence_pk"])
            self.case = get_case(self.request, self.kwargs["pk"])

        except HTTPError:
            raise Http404()

        if not rules.test_rule("can_licence_status_be_changed", self.request, self.licence):
            raise Http404()
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["case"] = self.case
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["cancel_url"] = reverse(
            "cases:case",
            kwargs={
                "queue_pk": self.kwargs["queue_pk"],
                "pk": self.case.id,
                "tab": "licences",
            },
        )
        return kwargs


class ChangeLicenceStatus(BaseChangeLicenceStatus):
    form_class = ChangeLicenceStatusForm
    template_name = "case/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["statuses"] = self.get_edit_licence_choices()
        kwargs["reference_code"] = self.licence["reference_code"]
        return kwargs

    def get_edit_licence_choices(self):
        licence_choice_map = {
            LicenceStatusEnum.REINSTATED: [
                LicenceStatusEnum.suspended_choice,
                LicenceStatusEnum.revoked_choice,
            ],
            LicenceStatusEnum.ISSUED: [
                LicenceStatusEnum.suspended_choice,
                LicenceStatusEnum.revoked_choice,
            ],
            LicenceStatusEnum.SUSPENDED: [
                LicenceStatusEnum.reinstated_choice,
                LicenceStatusEnum.revoked_choice,
            ],
        }
        status = self.licence.get("status")
        return licence_choice_map[status]

    def get_success_url(self):
        status = self.get_form().data["status"]
        return reverse(
            "cases:change_licence_status_confirmation",
            kwargs={
                "queue_pk": self.kwargs["queue_pk"],
                "pk": self.case.id,
                "licence_pk": self.kwargs["licence_pk"],
                "status": status,
            },
        )


class ChangeLicenceStatusConfirmation(SuccessMessageMixin, BaseChangeLicenceStatus):
    form_class = ChangeLicenceStatusConfirmationForm
    template_name = "case/form.html"
    success_message = "Licence status successfully changed"

    def dispatch(self, *args, **kwargs):
        self.status = self.kwargs["status"]
        return super().dispatch(*args, **kwargs)

    @expect_status(
        HTTPStatus.OK,
        "Error changing licence status",
        "Unexpected error changing licence status",
    )
    def update_licence_details(self, request, licence_id, data):
        return update_licence_details(request, licence_id, data)

    def form_valid(self, form):
        self.update_licence_details(self.request, self.licence["id"], {"status": self.status})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "cases:case",
            kwargs={
                "queue_pk": self.kwargs["queue_pk"],
                "pk": self.case.id,
                "tab": "licences",
            },
        )


class MoveCase(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.data = case
        self.form = move_case_form(request, get_queue(request, kwargs["queue_pk"]), case)
        self.action = put_case_queues
        self.context = {"case": case}
        self.success_message = cases.Manage.MoveCase.SUCCESS_MESSAGE
        self.success_url = reverse_lazy(
            "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk, "tab": "details"}
        )


class AttachDocuments(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        case = get_case(request, case_id)

        form = attach_documents_form(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "documents"})
        )

        return form_page(request, form, extra_data={"case_id": case_id, "case": case})

    def post(self, request, **kwargs):
        case_id = str(kwargs["pk"])
        data = []

        files = request.FILES.getlist("file")
        if len(files) != 1:
            return error_page(None, "We had an issue uploading your files. Try again later.")
        file = files[0]
        data.append(
            {
                "description": request.POST["description"],
                **get_document_data(file),
            }
        )

        # Send LITE API the file information
        case_documents, _ = post_case_documents(request, case_id, data)

        if "errors" in case_documents:
            if settings.DEBUG:
                raise APIError(case_documents["errors"])
            return error_page(None, "We had an issue uploading your files. Try again later.")

        return redirect(
            reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": case_id, "tab": "documents"})
        )


class Document(LoginRequiredMixin, View):
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


class RerunRoutingRules(SingleFormView):
    def init(self, request, **kwargs):
        self.action = put_rerun_case_routing_rules
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.context = {"case": case}
        self.form = rerun_routing_rules_confirmation_form()
        self.success_url = reverse_lazy(
            "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk}
        )

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        if not request.POST.get("confirm"):
            return form_page(
                request,
                self.get_form(),
                data=self.get_data(),
                errors={"confirm": ["select an option"]},
                extra_data=self.context,
            )
        elif request.POST.get("confirm") == "no":
            return redirect(self.success_url)

        return super(RerunRoutingRules, self).post(request, **kwargs)


class ReissueOGL(SingleFormView):
    def init(self, request, **kwargs):
        self.action = reissue_ogl
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.context = {"case": case}
        self.form = reissue_ogl_confirmation_form(self.object_pk, self.kwargs["queue_pk"])
        self.success_url = reverse_lazy(
            "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.object_pk}
        )

    def post(self, request, **kwargs):
        self.init(request, **kwargs)
        if not request.POST.get("confirm"):
            return form_page(
                request,
                self.get_form(),
                data=self.get_data(),
                errors={"confirm": [Manage.ReissueOGL.ERROR]},
                extra_data=self.context,
            )
        elif request.POST.get("confirm") == "False":
            return redirect(self.success_url)

        return super(ReissueOGL, self).post(request, **kwargs)
