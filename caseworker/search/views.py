from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from caseworker.cases.helpers.filters import case_filters_bar
from caseworker.cases.helpers.search import case_search_box
from caseworker.conf.constants import ALL_CASES_QUEUE_ID, Permission, UPDATED_CASES_QUEUE_ID
from caseworker.core.helpers import convert_parameters_to_query_params
from caseworker.queues.services import get_queue


class Search(TemplateView):
    def get(self, request, **kwargs):
        """
        Show a list of cases pertaining to the given queue
        """
        print(f"=====> {request.GET}, {request.user.default_queue}")
        queue = get_queue(request, request.user.default_queue)

        context = {
            "queue": queue,  # Used for showing current queue
            "search": case_search_box(request),
            "filters": case_filters_bar(request, queue),
            "params": convert_parameters_to_query_params(request.GET),  # Used for passing params to JS
            "case_officer": request.GET.get("case_officer"),  # Used for reading params dynamically
            "assigned_user": request.GET.get("assigned_user"),  # ""
            "team_advice_type": request.GET.get("team_advice_type"),  # ""
            "final_advice_type": request.GET.get("final_advice_type"),  # ""
            "updated_cases_banner_queue_id": UPDATED_CASES_QUEUE_ID,
        }
        return render(request, "search/search.html", context)
