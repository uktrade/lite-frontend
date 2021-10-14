from django.views.generic import FormView, TemplateView
from django.urls import reverse

from caseworker.advice import forms, services

import json

from django.utils.functional import cached_property

from core import client

from caseworker.cases.services import get_case
from caseworker.core.services import get_denial_reasons
from core.auth.views import LoginRequiredMixin

DECISION_TYPE_VERB_MAPPING = {
    "Approve": "approved",
    "Proviso": "approved with proviso",
    "Refuse": "refused",
    "Conflicting": "given conflicting advice",
}


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

    def get_context_data(self, **kwargs):
        return super().get_context_data(case=self.case, **kwargs,)


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
            return "/#refuse"


class GiveApprovalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    """
    Form to recommend approval advice for all products on the application
    """

    form_class = forms.GiveApprovalAdviceForm
    template_name = "advice/give-approval-advice.html"

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.post_approval_advice(self.request, case, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})


class RefusalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/refusal_advice.html"
    form_class = forms.RefusalAdviceForm

    def get_form_kwargs(self):
        """Overriding this so that I can pass denial_reasons
        to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs["denial_reasons"] = get_denial_reasons(self.request)
        return kwargs

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.post_refusal_advice(self.request, case, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})


class AdviceDetailView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    template_name = "advice/view_my_advice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case = context["case"]
        my_advice = services.filter_current_user_advice(case.advice, str(self.request.session["lite_api_user_id"]))
        nlr_products = services.filter_nlr_products(case["data"]["goods"])
        return {**context, "my_advice": my_advice, "nlr_products": nlr_products}


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
        return reverse("cases:view_my_advice", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})


class GetTeamsMixin:
    @cached_property
    def all_teams(self):
        response = client.get(self.request, "/teams/")
        response.raise_for_status()
        return response.json()["teams"]

    def get_context_data(self, **kwargs):
        return super().get_context_data(all_teams=self.all_teams, **kwargs,)


class QueueContextMixin:
    @property
    def queue_id(self):
        return str(self.kwargs["queue_pk"])

    @cached_property
    def queue(self):
        response = client.get(self.request, f"/queues/{self.queue_id}")
        response.raise_for_status()
        return response.json()

    def get_context_data(self, **kwargs):
        return super().get_context_data(queue=self.queue, **kwargs,)


class AdviceView(GetTeamsMixin, QueueContextMixin, CaseContextMixin, TemplateView):
    """This is POC ATM and should be removed with the first PR
    of advice. Currently, this is a TemplateView but it should
    be fairly simple to make this e.g. a SingleFormView.
    """

    template_name = "advice/view-advice.html"

    @property
    def destinations(self):
        return self.case.destinations

    # this is a rough schema for the grouped_advice
    # grouped_advice = [
    #     {
    #         "team": {team data},
    #         "advice": [
    #             {
    #                 "user": user,
    #                 "decision": approve/refuse etc,
    #                 "advice": [
    #                     {
    #                         "party_type": end user, third party etc,
    #                         "country": country,
    #                         "name": party name - of the organisation or individual. we don't get this from the api yet so using address for now,
    #                         "approved_products": [list of ids or serialized as names?],
    #                         "licence_condition": this will replace 'approve with proviso'
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # ]

    @property
    def grouped_advice(self):
        if not self.case["advice"]:
            return []
        grouped_advice = []
        for team in self.teams:
            team_advice = [advice for advice in self.case["advice"] if advice["user"]["team"]["id"] == team["id"]]
            team_advice_group = {
                "team": team,
                "advice": [],
            }
            team_users_unique = set([json.dumps(advice["user"]) for advice in self.case["advice"] if advice["user"]["team"]["id"] == team["id"]])
            team_users = [json.loads(user) for user in team_users_unique]

            for team_user in team_users:
                user_advice = [advice for advice in team_advice if advice["user"]["id"] == team_user["id"]]

                decisions = set([advice["type"]["value"] for advice in user_advice])

                for decision in decisions:
                    user_decision_advice_group = {
                        "user": team_user,
                        "decision": decision,
                        "decision_verb": DECISION_TYPE_VERB_MAPPING[decision],
                        "advice": [],
                    }
                    for destination in self.destinations:
                        advice = [a for a in user_advice if a[destination["type"]] is not None][0]
                        user_advice_destination = {
                            "type": destination["name"],
                            "address": destination["address"],
                            "licence_condition": advice["proviso"],
                            "country": destination["country"]["name"],
                            "advice": advice,
                        }
                        user_decision_advice_group["advice"].append(user_advice_destination)

                    team_advice_group["advice"].append(user_decision_advice_group)

                grouped_advice.append(team_advice_group)

        return grouped_advice

    @property
    def teams(self):
        teams_unique = set([json.dumps(advice["user"]["team"]) for advice in self.case["advice"]])
        return [json.loads(team) for team in teams_unique]

    def get_context_data(self, **kwargs):
        return super().get_context_data(advice=self.case["advice"], grouped_advice=self.grouped_advice, **kwargs,)
