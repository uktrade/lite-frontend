from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView
from django.urls import reverse
from requests.exceptions import HTTPError

from caseworker.advice import forms, services
from caseworker.advice.constants import DECISION_TYPE_VERB_MAPPING
from core import client
from caseworker.cases.services import get_case
from caseworker.core.services import get_denial_reasons
from caseworker.users.services import get_gov_user
from core.auth.views import LoginRequiredMixin


class CaseContextMixin:
    """Most advice views need a reference to the associated
    Case object. This mixin, injects a reference to the Case
    in the context.
    """

    @property
    def case_id(self):
        return str(self.kwargs["pk"])

    @property
    def case(self):
        return get_case(self.request, self.case_id)

    @property
    def caseworker_id(self):
        return str(self.request.session["lite_api_user_id"])

    @property
    def caseworker(self):
        data, _ = get_gov_user(self.request, self.caseworker_id)
        return data["user"]

    def unadvised_countries(self):
        """Returns a dict of countries for which advice has not been given"""
        dest_types = ("end_user", "ultimate_end_user", "consignee", "third_party")
        dests = {advice.get(dest_type) for dest_type in dest_types for advice in self.case.advice} - {None}
        return {
            dest["country"]["id"]: dest["country"]["name"] for dest in self.case.destinations if dest["id"] not in dests
        }

    def get_context(self, **kwargs):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ideally, we would probably want to not use the following
        # That said, if you look at the code, it is functional and
        # doesn't have anything to do with e.g. lite-forms
        # P.S. the case here is needed for rendering the base
        # template (layouts/case.html) from which we are inheriting.
        return {
            **context,
            **self.get_context(case=self.case),
            "case": self.case,
            "queue_pk": self.kwargs["queue_pk"],
            "caseworker": self.caseworker,
        }


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
            return reverse("cases:approve_all", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})
        else:
            return reverse("cases:refuse_all", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})


class GiveApprovalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    """
    Form to recommend approval advice for all products on the application
    """

    template_name = "advice/give-approval-advice.html"

    def get_form(self):
        if self.caseworker["team"]["name"] == "FCO":
            return forms.FCDOApprovalAdviceForm(self.unadvised_countries(), **self.get_form_kwargs())
        else:
            return forms.GiveApprovalAdviceForm(**self.get_form_kwargs())

    def form_valid(self, form):
        services.post_approval_advice(self.request, self.case, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})


class RefusalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/refusal_advice.html"

    def get_form(self):
        denial_reasons = get_denial_reasons(self.request)
        if self.caseworker["team"]["name"] == "FCO":
            return forms.FCDORefusalAdviceForm(denial_reasons, self.unadvised_countries(), **self.get_form_kwargs())
        else:
            return forms.RefusalAdviceForm(denial_reasons, **self.get_form_kwargs())

    def form_valid(self, form):
        services.post_refusal_advice(self.request, self.case, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})


class AdviceDetailView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/view_my_advice.html"
    form_class = forms.MoveCaseForwardForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_advice = services.filter_current_user_advice(self.case.advice, str(self.caseworker_id))
        nlr_products = services.filter_nlr_products(self.case["data"]["goods"])
        advice_completed = self.unadvised_countries() == {}
        return {**context, "my_advice": my_advice, "nlr_products": nlr_products, "advice_completed": advice_completed}

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


class EditAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    """
    Form to edit given advice for all products on the application
    """

    def get_form(self):
        case = get_case(self.request, self.kwargs["pk"])
        my_advice = services.filter_current_user_advice(case.advice, str(self.request.session["lite_api_user_id"]))
        advice = my_advice[0]

        if advice["type"]["key"] in ["approve", "proviso"]:
            self.advice_type = "approve"
            self.template_name = "advice/give-approval-advice.html"
            return forms.get_approval_advice_form_factory(advice)
        elif advice["type"]["key"] == "refuse":
            self.advice_type = "refuse"
            self.template_name = "advice/refusal_advice.html"
            denial_reasons = get_denial_reasons(self.request)
            return forms.get_refusal_advice_form_factory(advice, denial_reasons)
        else:
            raise ValueError("Invalid advice type encountered")

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        data = form.cleaned_data.copy()
        if self.advice_type == "approve":
            for field in form.changed_data:
                data[field] = self.request.POST.get(field)
            services.post_approval_advice(self.request, case, data)
        elif self.advice_type == "refuse":
            data["refusal_reasons"] = self.request.POST.get("refusal_reasons")
            data["denial_reasons"] = self.request.POST.getlist("denial_reasons")
            services.post_refusal_advice(self.request, case, data)
        else:
            raise ValueError("Unknown advice type")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})


class DeleteAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/delete-advice.html"
    form_class = forms.DeleteAdviceForm

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.delete_user_advice(self.request, case["id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:select_advice", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})


class AdviceView(LoginRequiredMixin, CaseContextMixin, TemplateView):
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

    @property
    def grouped_advice(self):
        if not self.case["advice"]:
            return []

        return self.group_advice()

    def group_user_advice(self, user_advice, destination):
        advice_item = [a for a in user_advice if a[destination["type"]] is not None][0]
        return {
            "type": destination["name"],
            "address": destination["address"],
            "licence_condition": advice_item["proviso"],
            "country": destination["country"]["name"],
            "advice": advice_item,
        }

    def group_user_decision_advice(self, user_advice, team_user, decision):
        user_advice_for_decision = [a for a in user_advice if a["type"]["value"] == decision and not a["good"]]
        return {
            "user": team_user,
            "decision": decision,
            "decision_verb": DECISION_TYPE_VERB_MAPPING[decision],
            "advice": [
                self.group_user_advice(user_advice_for_decision, destination)
                for destination in sorted(self.case.destinations, key=lambda d: d["name"])
                if [a for a in user_advice_for_decision if a[destination["type"]] is not None]
            ],
        }

    def group_team_user_advice(self, team, team_advice, team_user):
        user_advice = [advice for advice in team_advice if advice["user"]["id"] == team_user["id"]]
        decisions = sorted(set([advice["type"]["value"] for advice in user_advice]))
        return {
            "team": team,
            "advice": [
                self.group_user_decision_advice(user_advice, team_user, decision)
                for decision in decisions
                if [a for a in user_advice if a["type"]["value"] == decision]
            ],
        }

    def group_advice(self):
        grouped_advice = []

        for team in self.teams:
            team_advice = [
                advice
                for advice in self.case["advice"]
                if advice["user"]["team"]["id"] == team["id"] and not advice["good"]
            ]
            team_users = {
                advice["user"]["id"]: advice["user"]
                for advice in self.case["advice"]
                if advice["user"]["team"]["id"] == team["id"]
            }.values()
            grouped_advice += [self.group_team_user_advice(team, team_advice, team_user) for team_user in team_users]

        return grouped_advice

    def get_context(self, **kwargs):
        return {
            "queue": self.queue,
            "grouped_advice": self.grouped_advice,
        }


class ReviewCountersignView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    template_name = "advice/review_countersign.html"
    form_class = forms.CountersignAdviceForm

    def get_queues(self, users):
        queues = []
        for user in users:
            queue, _ = services.get_users_team_queues(self.request, user)
            queues.append(queue["queues"])
        return queues

    def get_context(self, **kwargs):
        context = super().get_context()
        advice_to_countersign = services.get_advice_to_countersign(self.case.advice, self.caseworker)
        advice_users_pks = list(advice_to_countersign.keys())
        queues = self.get_queues(advice_users_pks)
        context["formset"] = forms.get_queue_formset(self.form_class, queues)
        context["advice_to_countersign"] = advice_to_countersign.values()
        context["user_pks"] = advice_users_pks
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        advice_users_pks = context["user_pks"]
        queues = self.get_queues(advice_users_pks)
        formset = forms.get_queue_formset(self.form_class, queues, data=request.POST)
        if formset.is_valid():
            services.countersign_advice(request, self.case, self.caseworker, formset.cleaned_data)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response({**context, "formset": formset})

    def get_success_url(self):
        return reverse("cases:countersign_view", kwargs={**self.kwargs})


class ViewCountersignedAdvice(LoginRequiredMixin, CaseContextMixin, TemplateView):
    template_name = "advice/view_countersign.html"

    def get_context(self, **kwargs):
        context = super().get_context()
        advice_to_countersign = services.get_advice_to_countersign(self.case.advice, self.caseworker)
        context["advice_to_countersign"] = advice_to_countersign.values()
        context["review"] = False
        context["subtitle"] = f"Approved by {self.caseworker['team']['name']}"
        return context


class CountersignEditAdviceView(EditAdviceView):

    subtitle = (
        "Your changes as countersigner will be reflected on the recommendation that goes forward "
        "to the Licensing Unit. The original version will be recorded in the case history"
    )

    def get_context(self, **kwargs):
        return {**super().get_context(), "subtitle": self.subtitle, "edit": True}


class CountersignAdviceView(AdviceView):
    def get_context(self, **kwargs):
        return {**super().get_context(**kwargs), "countersign": True}


class ConsolidateAdviceView(AdviceView):
    def get_context(self, **kwargs):
        # For LU, we do not want to show the advice summary
        hide_advice = self.caseworker["team"]["name"] == "Licensing Unit"
        return {**super().get_context(**kwargs), "consolidate": True, "hide_advice": hide_advice}


class ReviewConsolidateView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/review_consolidate.html"

    def is_advice_approve_only(self):
        return all([a["type"]["key"] in ("approve", "proviso") for a in self.case.advice])

    def get_form(self):
        form_class = forms.ConsolidateSelectAdviceForm
        form_kwargs = self.get_form_kwargs()
        if self.kwargs.get("advice_type") == "approve" or self.is_advice_approve_only():
            form_class = forms.ConsolidateApprovalForm
        if self.kwargs.get("advice_type") == "refuse":
            form_kwargs["denial_reasons"] = get_denial_reasons(self.request)
            form_class = forms.RefusalAdviceForm
        return form_class(**form_kwargs)

    def get_context(self, **kwargs):
        context = super().get_context()
        advice_to_consolidate = services.get_advice_to_consolidate(self.case.advice)
        context["advice_to_consolidate"] = advice_to_consolidate.values()
        return context

    def form_valid(self, form):
        if isinstance(form, forms.ConsolidateApprovalForm):
            services.post_approval_advice(self.request, self.case, form.cleaned_data, level="team-advice")
        if isinstance(form, forms.RefusalAdviceForm):
            services.post_refusal_advice(self.request, self.case, form.cleaned_data, level="team-advice")
        return super().form_valid(form)

    def get_success_url(self):
        if self.kwargs.get("advice_type") is None:
            recommendation = self.request.POST.get("recommendation")
            if recommendation == "approve":
                return f"{self.request.path}approve/"
            else:
                return f"{self.request.path}refuse/"
        messages.add_message(self.request, messages.INFO, "Review successful.")
        return "/"
