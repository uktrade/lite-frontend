from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from core import client
from core.auth.views import LoginRequiredMixin


class MatchingDenials(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        data = []
        for match_id in request.POST.getlist("objects", []):
            data.append({"application": str(kwargs["pk"]), "denial": match_id, "category": kwargs["category"]})
        response = client.post(request, f"/applications/{kwargs['pk']}/denial-matches/", data)
        response.raise_for_status()
        return redirect(reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]}))


class RemoveMatchingDenials(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        data = {}
        data["objects"] = request.POST.getlist("objects", [])
        response = client.delete(request, f"/applications/{kwargs['pk']}/denial-matches/", data)
        response.raise_for_status()
        return redirect(reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]}))
