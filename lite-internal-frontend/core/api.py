from django.http import JsonResponse
from django.views.generic import TemplateView

from queues.services import get_cases_search_data


class Cases(TemplateView):
    def get(self, request, **kwargs):
        """
        Endpoint to enable access to the API /cases/ endpoint
        """
        hidden = request.GET.get("hidden")

        params = {"page": int(request.GET.get("page", 1))}
        for key, value in request.GET.items():
            if key != "flags[]":
                params[key] = value

        params["flags"] = request.GET.getlist("flags[]", [])

        if hidden:
            params["hidden"] = hidden

        data = get_cases_search_data(request, kwargs["pk"], params)
        return JsonResponse(data=data)
