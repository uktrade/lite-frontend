import rules

from logging import getLogger

from http import HTTPStatus

from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import (
    FormView,
    TemplateView,
    View,
)

from requests.exceptions import HTTPError

from core.auth.views import LoginRequiredMixin
from core.builtins.custom_tags import filter_advice_by_level
from core.decorators import expect_status
from core.exceptions import APIError
from core.helpers import (
    get_document_data,
    stream_document_response,
)
from core.services import stream_document

from lite_content.lite_internal_frontend import cases
from lite_content.lite_internal_frontend.cases import (
    CasePage,
    DoneWithCaseOnQueueForm,
    Manage,
)

from lite_forms.components import FiltersBar, TextInput
from lite_forms.generators import error_page, form_page
from lite_forms.helpers import conditional
from lite_forms.views import SingleFormView

from caseworker.advice.services import get_advice_tab_context
from caseworker.cases.forms.attach_documents import attach_documents_form
from caseworker.cases.forms.change_status import ChangeStatusForm
from caseworker.cases.forms.change_sub_status import ChangeSubStatusForm
from caseworker.cases.forms.change_licence_status import ChangeLicenseStatusForm
from caseworker.cases.forms.done_with_case import done_with_case_form
from caseworker.cases.forms.move_case import move_case_form
from caseworker.cases.forms.reissue_ogl_form import reissue_ogl_confirmation_form
from caseworker.cases.forms.rerun_routing_rules import rerun_routing_rules_confirmation_form
import caseworker.cases.helpers.advice as advice_helpers
from caseworker.cases.helpers.case import CaseView, Tabs, Slices
from caseworker.cases.services import (
    get_case,
    post_case_notes,
    put_case_queues,
    put_unassign_queues,
    put_rerun_case_routing_rules,
    put_application_status,
    reissue_ogl,
    post_case_documents,
    get_blocking_flags,
    get_case_sub_statuses,
    put_case_sub_status,
    get_licence_details,
)
from caseworker.compliance.services import get_compliance_licences
from caseworker.cases.services import get_case_basic_details
from caseworker.core.objects import Tab
from caseworker.core.services import get_status_properties, get_permissible_statuses
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
        ]

        return tabs

    def get_standard_application_tabs(self):
        tabs = self.get_tabs()
        tabs.append(self.get_notes_and_timelines_tab())
        tabs.append(self.get_assessment_tab())
        tabs.append(self.get_advice_tab())

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


class CaseDetail(CaseTabsMixin, CaseView):
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

        if final_advice and advice_helpers.check_user_permitted_to_give_final_advice(
            self.case.data["case_type"]["sub_type"]["key"], self.permissions
        ):
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

    def get_open_application(self):
        self.tabs = self.get_tabs()
        self.tabs.insert(1, Tabs.LICENCES)
        self.tabs.append(Tabs.ADVICE)
        self.slices = [
            Slices.GOODS,
            Slices.DESTINATIONS,
            Slices.OPEN_APP_PARTIES,
            Slices.SANCTION_MATCHES,
            conditional(self.case.data["inactive_parties"], Slices.DELETED_ENTITIES),
            Slices.LOCATIONS,
            *conditional(
                self.case.data["goodstype_category"]["key"] != "cryptographic",
                [Slices.END_USE_DETAILS, Slices.ROUTE_OF_GOODS],
                [],
            ),
            Slices.SUPPORTING_DOCUMENTS,
            conditional(self.case.data["export_type"]["key"] == "temporary", Slices.TEMPORARY_EXPORT_DETAILS),
        ]

        self.additional_context = self.get_advice_additional_context()

    def get_standard_application(self):
        self.tabs = self.get_standard_application_tabs()
        self.slices = [
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
        self.additional_context = self.get_advice_additional_context()

    def get_hmrc_application(self):
        self.slices = [
            conditional(self.case.data["reasoning"], Slices.HMRC_NOTE),
            Slices.GOODS,
            Slices.DESTINATIONS,
            Slices.LOCATIONS,
            Slices.SUPPORTING_DOCUMENTS,
        ]
        self.additional_context = self.get_advice_additional_context()

    def get_exhibition_clearance_application(self):
        self.tabs = self.get_tabs()
        self.tabs.insert(1, Tabs.LICENCES)
        self.tabs.append(Tabs.ADVICE)
        self.slices = [
            Slices.EXHIBITION_DETAILS,
            Slices.GOODS,
            Slices.LOCATIONS,
            Slices.SUPPORTING_DOCUMENTS,
        ]
        self.additional_context = self.get_advice_additional_context()

    def get_gifting_clearance_application(self):
        self.tabs = self.get_tabs()
        self.tabs.insert(1, Tabs.LICENCES)
        self.tabs.append(Tabs.ADVICE)
        self.slices = [Slices.GOODS, Slices.DESTINATIONS, Slices.LOCATIONS, Slices.SUPPORTING_DOCUMENTS]
        self.additional_context = self.get_advice_additional_context()

    def get_f680_clearance_application(self):
        self.tabs = self.get_tabs()
        self.tabs.insert(1, Tabs.LICENCES)
        self.tabs.append(Tabs.ADVICE)
        self.slices = [
            Slices.GOODS,
            Slices.DESTINATIONS,
            Slices.F680_DETAILS,
            Slices.END_USE_DETAILS,
            Slices.SUPPORTING_DOCUMENTS,
        ]
        self.additional_context = self.get_advice_additional_context()

    def get_end_user_advisory_query(self):
        self.slices = [Slices.END_USER_DETAILS]

    def get_open_registration(self):
        self.tabs = self.get_tabs()
        self.tabs.insert(1, Tabs.LICENCES)
        self.slices = [Slices.OPEN_GENERAL_LICENCE]

    def get_compliance_site(self):
        self.tabs = self.get_tabs()
        self.tabs.insert(1, Tabs.COMPLIANCE_LICENCES)
        self.slices = [Slices.COMPLIANCE_VISITS, Slices.OPEN_LICENCE_RETURNS]
        filters = FiltersBar(
            [
                TextInput(name="reference", title=cases.CasePage.LicenceFilters.REFERENCE),
            ]
        )
        self.additional_context = {
            "data": get_compliance_licences(
                self.request,
                self.case.id,
                self.request.GET.get("reference", ""),
                self.request.GET.get("page", 1),
            ),
            "licences_filters": filters,
        }

    def get_compliance_visit(self):
        self.tabs = self.get_tabs()
        self.tabs.insert(1, Tabs.COMPLIANCE_LICENCES)
        self.slices = [Slices.COMPLIANCE_VISIT_DETAILS]
        filters = FiltersBar(
            [
                TextInput(name="reference", title=cases.CasePage.LicenceFilters.REFERENCE),
            ]
        )
        self.additional_context = {
            "data": get_compliance_licences(
                self.request,
                self.case.data["site_case_id"],
                self.request.GET.get("reference", ""),
                self.request.GET.get("page", 1),
            ),
            "licences_filters": filters,
        }


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
    def put_case_status(self, request, case_id, data):
        return put_application_status(request, case_id, data)

    def form_valid(self, form):
        self.put_case_status(self.request, self.case.id, form.cleaned_data)
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


class ChangeLicenseStatus(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = ChangeLicenseStatusForm
    template_name = "case/form.html"

    def dispatch(self, *args, **kwargs):
        try:
            self.license = get_licence_details(self.request, self.kwargs["license_pk"])
            self.case = get_case(self.request, self.kwargs["pk"])

        except HTTPError:
            raise Http404()

        # if not rules.test_rule("can_licence_status_be_changed", self.request.user, self.license):
        #     raise Http404()

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["license"] = self.license
        context["case"] = self.case
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        cancel_url = reverse(
            "cases:case",
            kwargs={
                "queue_pk": self.kwargs["queue_pk"],
                "pk": self.case.id,
                "tab": "details",
            },
        )

        status_choices = [("issued", "Issued"), ("revoked", "Revoked"), ("suspended", "Suspended")]
        kwargs["statuses"] = status_choices
        kwargs["license"] = self.license
        kwargs["cancel_url"] = cancel_url

        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        status = self.license.get("status")
        if status:
            initial["status"] = status
        return initial


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
