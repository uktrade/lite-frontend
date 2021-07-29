from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from django.views.generic.edit import FormView

from core import client

from caseworker.auth.views import CaseworkerLoginRequiredMixin
from caseworker.cases.forms import external_data as forms
from caseworker.external_data.services import revoke_sanction
from caseworker.cases.services import get_case


class MatchingDenials(CaseworkerLoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = []
        for match_id in request.POST.getlist("objects", []):
            data.append({"application": str(kwargs["pk"]), "denial": match_id, "category": kwargs["category"]})
        response = client.post(request, f"/applications/{kwargs['pk']}/denial-matches/", data)
        response.raise_for_status()
        return redirect(reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]}))


class RemoveMatchingDenials(CaseworkerLoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = {}
        data["objects"] = request.POST.getlist("objects", [])
        response = client.delete(request, f"/applications/{kwargs['pk']}/denial-matches/", data)
        response.raise_for_status()
        return redirect(reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]}))


class SanctionRevokeView(CaseworkerLoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "external_data/sanction-revoke.html"
    success_message = "Sanction match successfully removed"
    form_class = forms.SanctionRevoke

    def get_context_data(self, **kwargs):
        case = get_case(self.request, self.kwargs["pk"])
        return super().get_context_data(
            case=case, queue_id=self.kwargs["queue_pk"], case_id=self.kwargs["pk"], **kwargs
        )

    def get_success_url(self):
        return reverse("cases:case", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})

    def form_valid(self, form):
        for pk in self.request.GET.getlist("objects"):
            revoke_sanction(request=self.request, pk=pk, comment=form.cleaned_data["comment"])
        return super().form_valid(form)
