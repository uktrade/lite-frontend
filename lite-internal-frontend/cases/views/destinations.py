from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.helpers import convert_dict_to_query_params


class AssignDestinationFlags(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])

        params = {}
        params["items"] = request.GET.getlist("destinations")
        params["level"] = "destinations"
        post_url = "?" + convert_dict_to_query_params(params)
        return redirect(reverse_lazy("cases:assign_flags", kwargs={"pk": case_id}) + post_url)
