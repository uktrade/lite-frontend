import itertools

from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.views.generic.edit import FormView

from core.auth.views import LoginRequiredMixin
from caseworker.cases.forms import case_assignment as forms

from caseworker.cases.services import delete_case_assignment, delete_case_officer
from caseworker.cases.services import get_case


class CaseAssignmentRemove(LoginRequiredMixin, FormView):
    template_name = "case/remove-allocation.html"
    form_class = forms.CaseAssignmentRemove

    def _get_adviser(self, case, assignment_id):
        all_assigned_users = itertools.chain.from_iterable(
            [queue_users for queue_users in case["assigned_users"].values()]
        )
        assigned_users_by_assignment_id = {user["assignment_id"]: user for user in all_assigned_users}
        try:
            return assigned_users_by_assignment_id[assignment_id]
        except KeyError:
            raise Http404

    def _get_adviser_identifier(self, case, assignment_id):
        adviser = self._get_adviser(case, assignment_id)
        adviser_identifier = adviser["email"]
        if adviser["first_name"] and adviser["last_name"]:
            adviser_identifier = f"{adviser['first_name']} {adviser['last_name']}"
        return adviser_identifier

    def get_case(self):
        return get_case(self.request, self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        case = self.get_case()
        context = super().get_context_data(
            case=case,
            queue_id=self.kwargs["queue_pk"],
            case_id=self.kwargs["pk"],
            adviser_identifier=self._get_adviser_identifier(case, self.request.GET.get("assignment_id")),
            **kwargs,
        )
        context["title"] = (
            f"{self.form_class.Layout.DOCUMENT_TITLE} - {case.reference_code} - {case.organisation['name']}"
        )

        return context

    def get_success_url(self):
        case = self.get_case()
        if case.case_type['sub_type']['key'] == 'f680_clearance':
            return reverse("cases:f680:details", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})
        return reverse(
                "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"], "tab": "details"}
            )

    def get_initial(self):
        return {"assignment_id": self.request.GET.get("assignment_id")}

    def form_valid(self, form):
        adviser_identifier = self._get_adviser_identifier(self.get_case(), form.cleaned_data["assignment_id"])
        response = delete_case_assignment(self.request, self.kwargs["pk"], form.cleaned_data["assignment_id"])
        if response.ok:
            messages.success(self.request, f"{adviser_identifier} was successfully removed as case adviser")
        else:
            messages.error(
                self.request,
                f"An error occurred when removing {adviser_identifier} as case adviser. Please try again later",
            )

        return super().form_valid(form)


class CaseOfficerRemove(LoginRequiredMixin, FormView):
    template_name = "case/remove-allocation.html"
    form_class = forms.CaseOfficerRemove

    def _get_case_officer(self, case):
        if case["case_officer"]:
            return case["case_officer"]
        else:
            raise Http404

    def _get_case_officer_name(self, case):
        case_officer = self._get_case_officer(case)
        if case_officer.get("first_name"):
            first_name = case_officer["first_name"]
            last_name = case_officer["last_name"]
            return f"{first_name} {last_name}"
        else:
            return case_officer["email"]

    def get_case(self):
        return get_case(self.request, self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        case = self.get_case()
        context = super().get_context_data(
            case=case,
            queue_id=self.kwargs["queue_pk"],
            case_id=self.kwargs["pk"],
            case_officer_name=self._get_case_officer_name(case),
            **kwargs,
        )
        context["title"] = (
            f"{self.form_class.Layout.DOCUMENT_TITLE} - {case.reference_code} - {case.organisation['name']}"
        )

        return context

    def get_success_url(self):
        default_success_url = reverse(
            "cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"], "tab": "details"}
        )
        return self.request.GET.get("return_to", default_success_url)

    def form_valid(self, form):
        case_officer_name = self._get_case_officer_name(self.get_case())
        _, status_code = delete_case_officer(self.request, self.kwargs["pk"])
        if status_code == 200:
            messages.success(
                self.request, f"{case_officer_name} was successfully removed as Licensing Unit case officer"
            )
        else:
            messages.error(
                self.request,
                f"An error occurred when removing {case_officer_name} as Licensing Unit case officer. Please try again later",
            )

        return super().form_valid(form)
