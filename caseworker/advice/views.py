from http import HTTPStatus
import sentry_sdk
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import FormView, TemplateView
from requests.exceptions import HTTPError

from caseworker.advice import forms, services, constants
from caseworker.advice.forms import DESNZTriggerListAssessmentForm, DESNZTriggerListAssessmentEditForm
from caseworker.cases.helpers.case import CaseworkerMixin
from caseworker.cases.services import get_case, get_final_decision_documents
from caseworker.cases.helpers.ecju_queries import has_open_queries
from caseworker.cases.views.main import CaseTabsMixin
from caseworker.core.helpers import get_organisation_documents
from caseworker.core.services import get_denial_reasons, group_denial_reasons
from caseworker.picklists.services import get_picklists_list
from caseworker.tau.summaries import get_good_on_application_tau_summary
from caseworker.users.services import get_gov_user

from caseworker.advice.constants import AdviceType
from core import client
from core.auth.views import LoginRequiredMixin
from core.constants import SecurityClassifiedApprovalsType, OrganisationDocumentType
from core.decorators import expect_status


class CaseContextMixin:
    """Most advice views need a reference to the associated
    Case object. This mixin, injects a reference to the Case
    in the context.
    """

    @property
    def case_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def case(self):
        return get_case(self.request, self.case_id)

    @cached_property
    def denial_reasons_display(self):
        denial_reasons_data = get_denial_reasons(self.request)
        return {denial_reason["id"]: denial_reason["display_value"] for denial_reason in denial_reasons_data}

    @property
    def security_approvals_classified_display(self):
        security_approvals = self.case["data"].get("security_approvals")
        if security_approvals:
            security_approvals_dict = dict(SecurityClassifiedApprovalsType.choices)
            return ", ".join([security_approvals_dict[approval] for approval in security_approvals])
        return ""

    @property
    def caseworker_id(self):
        return str(self.request.session["lite_api_user_id"])

    @property
    def caseworker(self):
        data, _ = get_gov_user(self.request, self.caseworker_id)
        return data["user"]

    @property
    def goods(self):
        for index, good_on_application in enumerate(self.case["data"]["goods"], start=1):
            good_on_application["line_number"] = index

        return self.case["data"]["goods"]

    def get_context(self, **kwargs):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ideally, we would probably want to not use the following
        # That said, if you look at the code, it is functional and
        # doesn't have anything to do with e.g. lite-forms
        # P.S. the case here is needed for rendering the base
        # template (layouts/case.html) from which we are inheriting.

        is_in_lu_team = self.caseworker["team"]["alias"] == services.LICENSING_UNIT_TEAM
        rejected_lu_countersignature = None
        if is_in_lu_team:
            rejected_lu_countersignature = self.rejected_countersign_advice()

        return {
            **context,
            **self.get_context(case=self.case),
            "case": self.case,
            "queue_pk": self.kwargs["queue_pk"],
            "caseworker": self.caseworker,
            "is_lu_countersigning": is_in_lu_team,
            "rejected_lu_countersignature": rejected_lu_countersignature,
        }

    def rejected_countersign_advice(self):
        """
        Return rejected countersignature. Due to the routing, there should only ever be one
        rejection (case will be returned to edit the advice once a rejection has occurred.
        """
        for cs in self.case.get("countersign_advice", []):
            if cs["valid"] and not cs["outcome_accepted"]:
                return cs
        return None


class DESNZNuclearMixin:
    def is_trigger_list_assessed(self, product):
        """Returns True if a product has been assessed for trigger list criteria"""
        return product.get("is_trigger_list_guidelines_applicable") in [True, False]

    @property
    def unassessed_trigger_list_goods(self):
        return [
            product
            for product in services.filter_trigger_list_products(self.goods)
            if not self.is_trigger_list_assessed(product)
        ]

    @property
    def assessed_trigger_list_goods(self):
        return [
            product
            for product in services.filter_trigger_list_products(self.goods)
            if self.is_trigger_list_assessed(product)
        ]


class CaseDetailView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    """This endpoint renders case detail panel. This will probably
    not be used stand-alone. This is useful for testing the case
    detail template ATM.
    """

    template_name = "advice/case_detail_example.html"


class SelectAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/select_advice.html"
    form_class = forms.SelectAdviceForm

    def get_success_url(self):
        recommendation = self.request.POST.get("recommendation")
        if recommendation == "approve_all":
            return reverse("cases:approve_all", kwargs=self.kwargs)
        else:
            return reverse("cases:refuse_all", kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, "security_approvals_classified_display": self.security_approvals_classified_display}


class GiveApprovalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    """
    Form to recommend approval advice for all products on the application
    """

    template_name = "advice/give-approval-advice.html"

    def get_form(self):
        if self.caseworker["team"]["alias"] == services.FCDO_TEAM:
            return forms.FCDOApprovalAdviceForm(
                services.unadvised_countries(self.caseworker, self.case),
                **self.get_form_kwargs(),
            )
        else:
            return forms.GiveApprovalAdviceForm(**self.get_form_kwargs())

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

    def form_valid(self, form):
        services.post_approval_advice(self.request, self.case, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "security_approvals_classified_display": self.security_approvals_classified_display,
            "title": f"{self.get_form().DOCUMENT_TITLE} - {self.case.reference_code} - {self.case.organisation['name']}",
        }


class RefusalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/refusal_advice.html"

    def get_form(self):
        denial_reasons = get_denial_reasons(self.request)
        choices = group_denial_reasons(denial_reasons)

        if self.caseworker["team"]["alias"] == services.FCDO_TEAM:
            return forms.FCDORefusalAdviceForm(
                choices,
                services.unadvised_countries(self.caseworker, self.case),
                **self.get_form_kwargs(),
            )
        else:
            return forms.RefusalAdviceForm(choices, **self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["refusal_reasons"] = get_picklists_list(
            self.request, type="standard_advice", disable_pagination=True, show_deactivated=False
        )
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        data["text"] = data["refusal_reasons"]
        services.post_refusal_advice(self.request, self.case, data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, "security_approvals_classified_display": self.security_approvals_classified_display}


class AdviceDetailView(LoginRequiredMixin, CaseTabsMixin, CaseContextMixin, DESNZNuclearMixin, FormView):
    template_name = "advice/view_my_advice.html"
    form_class = forms.MoveCaseForwardForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_advice = services.get_my_advice(self.case.advice, self.caseworker_id)
        nlr_products = services.filter_nlr_products(self.case["data"]["goods"])
        advice_completed = services.unadvised_countries(self.caseworker, self.case) == {}
        title = f"View recommendation for this case - {self.case.reference_code} - {self.case.organisation['name']}"
        return {
            **context,
            "title": title,
            "my_advice": my_advice.values(),
            "nlr_products": nlr_products,
            "advice_completed": advice_completed,
            "denial_reasons_display": self.denial_reasons_display,
            "tabs": self.get_standard_application_tabs(),
            "current_tab": "cases:view_my_advice",
            "security_approvals_classified_display": self.security_approvals_classified_display,
            "assessed_trigger_list_goods": self.assessed_trigger_list_goods,
            **services.get_advice_tab_context(self.case, self.caseworker, str(self.kwargs["queue_pk"])),
        }

    def form_valid(self, form):
        queue_id = str(self.kwargs["queue_pk"])
        try:
            services.move_case_forward(self.request, self.case.id, queue_id)
        except HTTPError as e:
            errors = e.response.json()["errors"]["queues"]
            for error in errors:
                form.add_error(None, error)
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("queues:cases", kwargs={"queue_pk": self.kwargs["queue_pk"]})


class EditAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    """
    Form to edit given advice for all products on the application
    """

    def get_form(self):
        my_advice = services.filter_current_user_advice(self.case.advice, self.caseworker_id)
        # The form that we are about to render lets the users edit e.g. approval/refusal reason
        # but the number of advice objects equals - destination x goods.
        # That said, approval/refusal reasons are the same for all of these objects so we
        # can take the first object and populate the form from it.
        # TODO: The following is a bit fragile and may result in an IndexError. We have
        # put sentry context that includes self.caseworker and self.case.advice in order
        # to debug when this goes south.
        sentry_sdk.set_context("caseworker", self.caseworker)
        sentry_sdk.set_context("advice", {"advice": self.case.advice})
        advice = my_advice[0]
        approval_refusal_reasons = get_picklists_list(
            self.request, type="standard_advice", disable_pagination=True, show_deactivated=False
        )

        if advice["type"]["key"] in ["approve", "proviso"]:
            self.template_name = "advice/give-approval-advice.html"
            proviso = get_picklists_list(self.request, type="proviso", disable_pagination=True, show_deactivated=False)
            footnote_details = get_picklists_list(
                self.request, type="footnotes", disable_pagination=True, show_deactivated=False
            )

            return forms.get_approval_advice_form_factory(
                advice, approval_refusal_reasons, proviso, footnote_details, self.request.POST
            )
        elif advice["type"]["key"] == "refuse":
            self.template_name = "advice/refusal_advice.html"
            denial_reasons = get_denial_reasons(self.request)
            choices = group_denial_reasons(denial_reasons)
            return forms.get_refusal_advice_form_factory(advice, choices, approval_refusal_reasons, self.request.POST)
        else:
            raise ValueError("Invalid advice type encountered")

    def advised_countries(self):
        """Returns a list of countries for which advice has given by the current user."""
        dest_types = constants.DESTINATION_TYPES
        advice = services.filter_current_user_advice(self.case.advice, self.caseworker_id)
        advised_on = {a.get(dest_type) for dest_type in dest_types for a in advice if a.get(dest_type) is not None}
        return [dest["country"]["id"] for dest in self.case.destinations if dest["id"] in advised_on]

    def form_valid(self, form):
        data = form.cleaned_data
        # When an FCO officer edits the advice, we don't allow for changing the countries
        # & therefore, we render the normal forms and not the FCO ones.
        # This means that here data here doesn't include the list of countries for which
        # the advice should be applied and so we pop that in using a method.
        if self.caseworker["team"]["alias"] == services.FCDO_TEAM:
            data["countries"] = self.advised_countries()
        if isinstance(form, forms.GiveApprovalAdviceForm):
            services.post_approval_advice(self.request, self.case, data)
        elif isinstance(form, forms.RefusalAdviceForm):
            data["text"] = data["refusal_reasons"]
            services.post_refusal_advice(self.request, self.case, data)
        else:
            raise ValueError("Unknown advice type")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["security_approvals_classified_display"] = self.security_approvals_classified_display
        context["edit"] = True
        return context


class DeleteAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/delete-advice.html"
    form_class = forms.DeleteAdviceForm

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.delete_user_advice(self.request, case["id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:select_advice", kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["security_approvals_classified_display"] = self.security_approvals_classified_display
        return context


class AdviceView(LoginRequiredMixin, CaseTabsMixin, CaseContextMixin, DESNZNuclearMixin, CaseworkerMixin, TemplateView):
    template_name = "advice/view-advice.html"

    @property
    def queue_id(self):
        return str(self.kwargs["queue_pk"])

    @property
    def queue(self):
        response = client.get(self.request, f"/queues/{self.queue_id}")
        response.raise_for_status()
        return response.json()

    @property
    def teams(self):
        return sorted(
            {advice["user"]["team"]["id"]: advice["user"]["team"] for advice in self.case["advice"]}.values(),
            key=lambda a: a["name"],
        )

    def can_advise(self):
        if self.caseworker["team"]["alias"] == services.FCDO_TEAM:
            # FCO cannot advice when all the destinations are already covered
            return services.unadvised_countries(self.caseworker, self.case) != {}
        return True

    def get_context(self, **kwargs):
        context = {
            "title": f"Make recommendation for this case - {self.case.reference_code} - {self.case.organisation['name']}",
            "queue": self.queue,
            "can_advise": self.can_advise(),
            "denial_reasons_display": self.denial_reasons_display,
            "security_approvals_classified_display": self.security_approvals_classified_display,
            "assessed_trigger_list_goods": self.assessed_trigger_list_goods,
            "unassessed_trigger_list_goods": self.unassessed_trigger_list_goods,
            "tabs": self.get_tabs_by_case_type(self.case.sub_type),
            "current_tab": "cases:advice_view",
            **services.get_advice_tab_context(
                self.case,
                self.caseworker,
                self.queue_id,
            ),
        }
        return context


class ReviewCountersignView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    template_name = "advice/review_countersign.html"
    form_class = forms.CountersignAdviceForm

    def get_context(self, **kwargs):
        context = super().get_context()
        advice = services.get_advice_to_countersign(self.case.advice, self.caseworker)
        context["formset"] = forms.get_formset(self.form_class, len(advice))
        context["advice_to_countersign"] = advice.values()
        context["denial_reasons_display"] = self.denial_reasons_display
        context["security_approvals_classified_display"] = self.security_approvals_classified_display
        context[
            "title"
        ] = f"{self.form_class.DOCUMENT_TITLE} - {self.case.reference_code} - {self.case.organisation['name']}"
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        advice = context["advice_to_countersign"]
        formset = forms.get_formset(self.form_class, len(advice), data=request.POST)
        if formset.is_valid():
            services.countersign_advice(request, self.case, self.caseworker, formset.cleaned_data)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response({**context, "formset": formset})

    def get_success_url(self):
        return reverse("cases:countersign_view", kwargs=self.kwargs)


class ViewCountersignedAdvice(AdviceDetailView):
    template_name = "advice/view_countersign.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        is_in_lu_team = self.caseworker["team"]["alias"] == services.LICENSING_UNIT_TEAM
        if is_in_lu_team:
            rejected_lu_countersignature = self.rejected_countersign_advice()
            if rejected_lu_countersignature:
                kwargs["move_case_button_label"] = "Move case back"

        return kwargs

    def can_edit(self, advice_to_countersign):
        """Determine of the current user can edit the countersign comments.
        This will be the case if the current user made those comments.
        """
        countersigned_by = services.get_countersigners(advice_to_countersign)
        return self.caseworker_id in countersigned_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advice_to_countersign = services.get_advice_to_countersign(self.case.advice, self.caseworker)
        context["advice_to_countersign"] = advice_to_countersign.values()
        context["can_edit"] = self.can_edit(advice_to_countersign)
        context["lu_can_edit"] = self.caseworker_id in services.get_countersigners_decision_advice(
            self.case, self.caseworker
        )
        context["denial_reasons_display"] = self.denial_reasons_display
        context["current_tab"] = "cases:countersign_view"
        context["show_rejected_countersignatures"] = True

        return context


class ReviewCountersignDecisionAdviceView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    template_name = "advice/review_countersign.html"
    form_class = forms.CountersignDecisionAdviceForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context(self, **kwargs):
        context = super().get_context()
        advice = services.get_advice_to_countersign(self.case.advice, self.caseworker)
        context["formset"] = forms.get_formset(self.form_class, len(advice))
        context["advice_to_countersign"] = advice.values()
        context["lu_can_edit"] = self.caseworker_id in services.get_countersigners_decision_advice(
            self.case, self.caseworker
        )
        context["denial_reasons_display"] = self.denial_reasons_display
        context["security_approvals_classified_display"] = self.security_approvals_classified_display
        return context

    def post(self, request, *args, **kwargs):
        queue_id = str(kwargs["queue_pk"])
        context = self.get_context_data()
        advice = context["advice_to_countersign"]
        formset = forms.get_formset(self.form_class, len(advice), data=request.POST)
        if formset.is_valid():
            services.countersign_decision_advice(request, self.case, queue_id, self.caseworker, formset.cleaned_data)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response({**context, "formset": formset})

    def get_success_url(self):
        return reverse("cases:countersign_view", kwargs=self.kwargs)


class EditCountersignDecisionAdviceView(ReviewCountersignDecisionAdviceView):
    def get_data(self, countersign_advice):
        data = []
        for item in countersign_advice.values():
            outcome_accepted = item[0].get("outcome_accepted")
            reason_field = "approval_reasons" if outcome_accepted else "rejected_reasons"
            data.append({"outcome_accepted": outcome_accepted, reason_field: item[0].get("reasons")})
        return data

    def get_context(self, **kwargs):
        context = super().get_context()
        countersign_advice = services.get_countersign_decision_advice_by_user(self.case, self.caseworker)
        context["countersign_advice"] = countersign_advice
        data = self.get_data(countersign_advice)
        context["formset"] = forms.get_formset(self.form_class, len(countersign_advice), initial=data)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        formset = forms.get_formset(self.form_class, len(context["countersign_advice"]), data=request.POST)
        if formset.is_valid():
            # single form item returned currently so using it to update decisions
            services.update_countersign_decision_advice(request, self.case, self.caseworker, formset.cleaned_data)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response({**context, "formset": formset})


class CountersignEditAdviceView(ReviewCountersignView):
    def get_data(self, advice):
        return [{"approval_reasons": a[0].get("countersign_comments")} for a in advice]

    def get_context(self, **kwargs):
        context = super().get_context()
        advice = context["advice_to_countersign"]
        data = self.get_data(advice)
        context["formset"] = forms.get_formset(self.form_class, len(advice), initial=data)
        return context


class CountersignAdviceView(AdviceView):
    def get_context(self, **kwargs):
        return {**super().get_context(**kwargs), "countersign": True}


class ConsolidateAdviceView(AdviceView):
    def get_context(self, **kwargs):
        return {**super().get_context(**kwargs), "consolidate": True}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["current_tab"] = "cases:consolidate_advice_view"
        return context


class ReviewConsolidateView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/review_consolidate.html"

    def is_advice_approve_only(self):
        approve_advice_types = ("approve", "proviso", "no_licence_required")
        return all(a["type"]["key"] in approve_advice_types for a in self.case.advice)

    def get_form(self):
        form_kwargs = self.get_form_kwargs()

        if self.kwargs.get("advice_type") == AdviceType.REFUSE:
            denial_reasons = get_denial_reasons(self.request)
            choices = group_denial_reasons(denial_reasons)
            if self.caseworker["team"]["alias"] == services.LICENSING_UNIT_TEAM:
                return forms.LUConsolidateRefusalForm(choices=choices, **form_kwargs)
            form_kwargs["refusal_reasons"] = get_picklists_list(
                self.request, type="standard_advice", disable_pagination=True, show_deactivated=False
            )
            return forms.RefusalAdviceForm(choices, **form_kwargs)

        if self.kwargs.get("advice_type") == AdviceType.APPROVE or self.is_advice_approve_only():
            form_kwargs["approval_reason"] = get_picklists_list(
                self.request, type="standard_advice", disable_pagination=True, show_deactivated=False
            )
            form_kwargs["proviso"] = get_picklists_list(
                self.request, type="proviso", disable_pagination=True, show_deactivated=False
            )
            form_kwargs["footnote_details"] = get_picklists_list(
                self.request, type="footnotes", disable_pagination=True, show_deactivated=False
            )

            team_alias = self.caseworker["team"].get("alias", None)
            return forms.ConsolidateApprovalForm(team_alias=team_alias, **form_kwargs)

        team_name = self.caseworker["team"]["name"]
        return forms.ConsolidateSelectAdviceForm(team_name=team_name, **form_kwargs)

    def get_context(self, **kwargs):
        context = super().get_context()
        team_alias = (
            self.caseworker["team"]["alias"] if self.caseworker["team"]["alias"] else self.caseworker["team"]["id"]
        )
        advice_to_consolidate = services.get_advice_to_consolidate(self.case.advice, team_alias)
        context["advice_to_consolidate"] = advice_to_consolidate.values()
        context["denial_reasons_display"] = self.denial_reasons_display
        context["security_approvals_classified_display"] = self.security_approvals_classified_display
        title = (
            f"Review and combine case recommendation - {self.case.reference_code} - {self.case.organisation['name']}"
        )
        if self.kwargs.get("advice_type") == "refuse":
            title = f"Licence refused for case - {self.case.reference_code} - {self.case.organisation['name']}"

        context["title"] = title

        return context

    def form_valid(self, form):
        user_team_alias = self.caseworker["team"]["alias"]
        level = "final-advice" if user_team_alias == services.LICENSING_UNIT_TEAM else "team-advice"
        try:
            if isinstance(form, forms.ConsolidateApprovalForm):
                services.post_approval_advice(self.request, self.case, form.cleaned_data, level=level)
            if isinstance(form, (forms.LUConsolidateRefusalForm, forms.RefusalAdviceForm)):
                data = form.cleaned_data
                if data.get("refusal_note"):
                    data["text"] = data["refusal_note"]
                    data["is_refusal_note"] = True
                if data.get("refusal_reasons"):
                    data["text"] = data["refusal_reasons"]

                services.post_refusal_advice(self.request, self.case, data, level=level)
        except HTTPError as e:
            errors = e.response.json()["errors"]
            form.add_error(None, errors)
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        if self.kwargs.get("advice_type") is None:
            recommendation = self.request.POST.get("recommendation")
            if recommendation == "approve":
                return f"{self.request.path}approve/"
            if recommendation == "refuse":
                return f"{self.request.path}refuse/"
        return reverse("cases:consolidate_view", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})


class ConsolidateEditView(ReviewConsolidateView):
    """
    Form to edit consolidated advice.
    """

    def setup(self, request, *args, **kwargs):
        """User the setup method to pre-set kwargs["advice_type"] so
        that we don't render the select-advice form.
        """
        super().setup(request, *args, **kwargs)

        user_team_alias = self.caseworker["team"]["alias"]
        level = "final" if user_team_alias == services.LICENSING_UNIT_TEAM else "team"
        team_advice = services.filter_advice_by_level(self.case.advice, [level])
        # TODO: The following is a bit fragile and may result in an IndexError. We have
        # put sentry context that includes self.caseworker and self.case.advice in order
        # to debug when this goes south.
        sentry_sdk.set_context("caseworker", self.caseworker)
        sentry_sdk.set_context("advice", {"advice": self.case.advice})
        self.advice = services.filter_advice_by_team(team_advice, user_team_alias)[0]
        self.advice_type = self.advice["type"]["key"]
        self.kwargs["advice_type"] = "refuse" if self.advice_type == "refuse" else "approve"

    def get_approval_data(self):
        return {
            "approval_reasons": self.advice["text"],
            "proviso": self.advice["proviso"],
        }

    def get_refusal_data(self):
        denial_reasons = [r for r in self.advice["denial_reasons"]]

        return {
            "refusal_reasons": self.advice["text"],
            "refusal_note": self.advice["text"],
            "denial_reasons": denial_reasons,
        }

    def get_data(self):
        if self.advice_type == "refuse":
            return self.get_refusal_data()
        return self.get_approval_data()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["data"] = self.request.POST or self.get_data()
        return kwargs

    def form_valid(self, form):
        user_team_alias = self.caseworker["team"]["alias"]

        # A new method added to API to support update of 'final' level advice
        # hence only LU can use these methods at the moment
        if user_team_alias != services.LICENSING_UNIT_TEAM:
            return super().form_valid(form)

        level = "final-advice"
        try:
            if isinstance(form, forms.ConsolidateApprovalForm):
                services.update_advice(
                    self.request, self.case, self.caseworker, self.advice_type, form.cleaned_data, level
                )
            if isinstance(form, forms.LUConsolidateRefusalForm):
                # If refusal_note exists then we will convert the old Advice to refusal note from refusal reason
                # ATM this function update_advice is only being used by LU final-level for updating.
                # OGDs use post_refusal_advice function for both Create and Update
                data = form.cleaned_data
                if data["refusal_note"]:
                    data["text"] = data["refusal_note"]
                    data["is_refusal_note"] = True

                services.update_advice(self.request, self.case, self.caseworker, self.advice_type, data, level)
        except HTTPError as e:
            errors = e.response.json()["errors"]
            form.add_error(None, errors)
            return super().form_invalid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("cases:consolidate_view", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})


class ViewConsolidatedAdviceView(AdviceView, FormView):
    form_class = forms.MoveCaseForwardForm

    def get_lu_countersign_required(self, rejected_lu_countersignature):
        case_flag_ids = {flag["id"] for flag in self.case.all_flags}
        lu_countersign_flags = services.LU_COUNTERSIGN_FLAGS

        lu_countersign_flags.update({services.MANPADS_ID, services.AP_LANDMINE_ID})

        countersign_orders = []
        countersign_required = case_flag_ids.intersection(lu_countersign_flags)
        if countersign_required:
            countersign_orders = [services.FIRST_COUNTERSIGN]
        senior_manager_countersign_required = case_flag_ids.intersection(
            {services.LU_SR_MGR_CHECK_REQUIRED_ID, services.MANPADS_ID}
        )
        if senior_manager_countersign_required:
            countersign_orders = [services.FIRST_COUNTERSIGN, services.SECOND_COUNTERSIGN]

        if rejected_lu_countersignature:
            lu_countersign_required = False
        else:
            countersign_advice = self.case.get("countersign_advice", [])
            are_all_countersign_orders_accepted = []
            for order in countersign_orders:
                filtered_countersign_advice = services.filter_countersign_advice_by_order(countersign_advice, order)
                are_all_countersign_orders_accepted.append(
                    len(filtered_countersign_advice) > 0
                    and all(item["outcome_accepted"] for item in filtered_countersign_advice)
                )

            lu_countersign_required = not all(are_all_countersign_orders_accepted)

        return lu_countersign_required

    def get_context(self, **kwargs):
        user_team_alias = self.caseworker["team"]["alias"]
        consolidated_advice = []
        if user_team_alias in [services.LICENSING_UNIT_TEAM, services.MOD_ECJU_TEAM]:
            consolidated_advice = services.get_consolidated_advice(self.case.advice, user_team_alias)
        nlr_products = services.filter_nlr_products(self.case["data"]["goods"])

        lu_countersign_required = False
        finalise_case = False

        # Hack to ensure that F680 cases can be finalised by MOD-ECJU
        if user_team_alias == services.MOD_ECJU_TEAM and self.case.case_type["reference"]["key"] == "f680":
            finalise_case = True

        if user_team_alias == services.LICENSING_UNIT_TEAM:
            rejected_lu_countersignature = self.rejected_countersign_advice()
            lu_countersign_required = self.get_lu_countersign_required(rejected_lu_countersignature)
            finalise_case = not (lu_countersign_required or rejected_lu_countersignature)

        refusal_note = [advice for advice in consolidated_advice if advice["is_refusal_note"]]

        # Only show an inform letter on the decision documents
        decisions, _ = get_final_decision_documents(self.request, self.case.id)
        decision_documents = {key: value for key, value in decisions.get("documents", {}).items() if key == "inform"}
        return {
            **super().get_context(**kwargs),
            "consolidated_advice": consolidated_advice,
            "nlr_products": nlr_products,
            "denial_reasons_display": self.denial_reasons_display,
            "lu_countersign_required": lu_countersign_required,
            "finalise_case": finalise_case,
            "case": self.case,
            "decisions": decision_documents,
            "queue_id": self.queue_id,
            "refusal_note": refusal_note,
            "has_open_queries": has_open_queries(self.request, self.case_id),
        }

    def form_valid(self, form):
        try:
            services.move_case_forward(self.request, self.case.id, self.queue_id)
        except HTTPError as e:
            errors = e.response.json()["errors"]["queues"]
            for error in errors:
                form.add_error(None, error)
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("queues:cases", kwargs={"queue_pk": self.kwargs["queue_pk"]})


class DESNZAssessmentBase:
    @cached_property
    def organisation_documents(self):
        """This property will collect the org documents that we need to access
        in the template e.g. section 5 certificate etc."""
        return get_organisation_documents(
            self.case,
            self.queue_id,
        )

    @expect_status(
        HTTPStatus.OK,
        "Error saving trigger list assessment",
        "Unexpected error saving trigger list assessment",
    )
    def post_trigger_list_assessment(self, request, case_id, selected_good_ids, data):
        good_on_application_map = {
            item["id"]: {"application": str(case_id), "good": item["good"]["id"]}
            for item in services.filter_trigger_list_products(self.case["data"]["goods"])
        }

        data = [
            {
                "id": item_id,
                **good_on_application_map[item_id],
                **data,
            }
            for item_id in selected_good_ids
        ]

        return services.post_trigger_list_assessment(self.request, case_id=self.kwargs["pk"], data=data)


class DESNZProductAssessmentView(AdviceView, DESNZNuclearMixin, DESNZAssessmentBase, FormView):
    """This renders trigger list product assessment for DESNZ Nuclear"""

    template_name = "advice/trigger_list_home.html"
    form_class = DESNZTriggerListAssessmentForm

    def get_success_url(self):
        if self.case:
            # Clear the cached case in order to get the updated case from the DB.
            del self.case
        if len(self.unassessed_trigger_list_goods) == 0:
            return reverse("cases:advice_view", kwargs=self.kwargs)

        return self.request.path

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()

        form_kwargs["request"] = self.request
        form_kwargs["queue_pk"] = self.queue_id
        form_kwargs["application_pk"] = self.case["id"]
        form_kwargs["organisation_documents"] = self.organisation_documents
        rfd_certificate = self.organisation_documents.get("rfd_certificate")
        is_user_rfd = bool(rfd_certificate) and not rfd_certificate["is_expired"]
        form_kwargs["is_user_rfd"] = is_user_rfd
        form_kwargs["goods"] = {item["id"]: item for item in self.unassessed_trigger_list_goods}

        return form_kwargs

    def get_unassessed_trigger_list_goods_json(self, unassessed_trigger_list_goods):
        goods_json = [
            {
                "id": good_on_application["id"],
                "name": good_on_application["good"]["name"],
            }
            for good_on_application in unassessed_trigger_list_goods
        ]
        return goods_json

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "case": self.case,
            "queue_pk": self.queue_id,
            "assessed_trigger_list_goods": self.assessed_trigger_list_goods,
            "unassessed_trigger_list_goods": self.unassessed_trigger_list_goods,
            "unassessed_trigger_list_goods_json": self.get_unassessed_trigger_list_goods_json(
                self.unassessed_trigger_list_goods,
            ),
        }

    def form_valid(self, form):
        data = {**form.cleaned_data}
        selected_good_ids = data.pop("goods", [])

        self.post_trigger_list_assessment(
            self.request, case_id=self.kwargs["pk"], selected_good_ids=selected_good_ids, data=data
        )

        return super().form_valid(form)


class DESNZProductAssessmentEditView(AdviceView, DESNZNuclearMixin, DESNZAssessmentBase, FormView):
    """This renders editing of trigger list product assessment for DESNZ Nuclear"""

    template_name = "advice/trigger_list_edit.html"
    form_class = DESNZTriggerListAssessmentEditForm

    def get_success_url(self):
        return reverse("cases:advice_view", kwargs={"queue_pk": self.queue_id, "pk": self.case_id})

    def get_good_on_application(self):
        selected_id = str(self.kwargs["good_on_application_id"])
        for good_on_application in self.assessed_trigger_list_goods:
            if good_on_application["id"] == selected_id:
                return good_on_application
        raise Http404

    def get_good_on_application_summary(self, good):
        organisation_documents = {
            document["document_type"]: document for document in self.organisation_documents.values()
        }
        rfd_certificate = organisation_documents.get(OrganisationDocumentType.RFD_CERTIFICATE)
        is_user_rfd = bool(rfd_certificate) and not rfd_certificate["is_expired"]

        summary = get_good_on_application_tau_summary(
            self.request,
            good,
            self.queue_id,
            self.case["id"],
            is_user_rfd,
            organisation_documents,
        )

        return summary

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()

        form_kwargs["request"] = self.request
        form_kwargs["queue_pk"] = self.queue_id
        form_kwargs["application_pk"] = self.case["id"]
        form_kwargs["organisation_documents"] = self.organisation_documents
        rfd_certificate = self.organisation_documents.get("rfd_certificate")
        is_user_rfd = bool(rfd_certificate) and not rfd_certificate["is_expired"]
        form_kwargs["is_user_rfd"] = is_user_rfd

        good_on_application = self.get_good_on_application()

        form_kwargs["data"] = self.request.POST or {
            "is_trigger_list_guidelines_applicable": good_on_application["is_trigger_list_guidelines_applicable"],
            "is_nca_applicable": good_on_application["is_nca_applicable"],
            "nsg_assessment_note": good_on_application["nsg_assessment_note"],
        }

        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        good_on_application = self.get_good_on_application()
        summary = self.get_good_on_application_summary(good_on_application)
        return {
            **context,
            "case": self.case,
            "queue_id": self.queue_id,
            "good_on_application": good_on_application,
            "assessed_trigger_list_goods": self.assessed_trigger_list_goods,
            "summary": summary,
        }

    def form_valid(self, form):
        data = {**form.cleaned_data}
        selected_good_ids = [str(self.kwargs["good_on_application_id"])]

        self.post_trigger_list_assessment(
            self.request, case_id=self.kwargs["pk"], selected_good_ids=selected_good_ids, data=data
        )

        return super().form_valid(form)


class DESNZProductClearAssessmentsView(AdviceView, DESNZNuclearMixin, DESNZAssessmentBase):
    """Clears the assessments for all the goods on the current case."""

    template_name = "advice/clear_trigger_list_assesment.html"

    def post(self, request, queue_pk, pk):
        data = {"is_trigger_list_guidelines_applicable": None, "is_nca_applicable": None, "nsg_assessment_note": ""}
        selected_good_ids = [product["id"] for product in self.assessed_trigger_list_goods]

        self.post_trigger_list_assessment(
            self.request, case_id=self.case.id, selected_good_ids=selected_good_ids, data=data
        )
        return redirect(reverse("cases:assess_trigger_list", kwargs={"queue_pk": queue_pk, "pk": pk}))
