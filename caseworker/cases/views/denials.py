from django.http import QueryDict
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from caseworker.cases.forms.denial_forms import DenialSearchForm
from caseworker.cases.services import get_case
from caseworker.external_data.services import search_denials
from caseworker.cases.constants import PartyType


class Denials(LoginRequiredMixin, FormView):
    template_name = "case/denial-for-case.html"
    form_class = DenialSearchForm

    @cached_property
    def case(self):
        return get_case(self.request, self.kwargs["pk"])

    @property
    def parties_to_search(self):
        parties_to_search = []
        for party_type in self.request.GET.keys():
            if party_type in [PartyType.END_USER, PartyType.CONSIGNEE]:
                parties_to_search.append(self.case.data[party_type])

            if party_type == PartyType.ULTIMATE_END_USER:
                selected_ultimate_end_user_ids = self.request.GET.getlist(party_type)
                parties_to_search.extend(
                    [
                        entity
                        for entity in self.case.data["ultimate_end_users"]
                        if entity["id"] in selected_ultimate_end_user_ids
                    ]
                )

            if party_type == PartyType.THIRD_PARTY:
                selected_third_party_ids = self.request.GET.getlist(party_type)
                parties_to_search.extend(
                    [entity for entity in self.case.data["third_parties"] if entity["id"] in selected_third_party_ids]
                )
        return parties_to_search

    def get_search_filter(self, form=None):
        """
        This is building the query_string that will be executed directly by the backend
        The field query is contained within () without this ES gets confused and searches
        across columns even when the column name is given.
        """
        filter = {
            "country": set(),
        }
        for party in self.parties_to_search:
            filter["country"].add(party["country"]["name"])

        if not form:
            search_filter = []
            for party in self.parties_to_search:
                search_filter.append(f'name:({party["name"]})')
                search_filter.append(f'address:({party["address"]})')
            search_string = " ".join(search_filter)
        else:
            search_string = form.cleaned_data["search_string"]

        return search_string, filter

    def get_initial(self):
        search_string, _ = self.get_search_filter()
        return {
            "search_string": search_string,
        }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        form_action = reverse(
            "cases:denials",
            kwargs={
                "queue_pk": str(self.kwargs["queue_pk"]),
                "pk": str(self.kwargs["pk"]),
            },
        )

        query = QueryDict("page=1", mutable=True)
        for party_type in [
            PartyType.END_USER,
            PartyType.CONSIGNEE,
            PartyType.ULTIMATE_END_USER,
            PartyType.THIRD_PARTY,
        ]:
            items = self.request.GET.getlist(party_type)
            if items:
                query.setlist(
                    party_type,
                    items,
                )

        kwargs["form_action"] = f"{form_action}?{query.urlencode()}"

        return kwargs

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, form=None, **kwargs):
        ctx = super().get_context_data(**kwargs)

        total_pages = 0
        count = 0
        results = []

        search, filter = self.get_search_filter(form)
        if search:
            page = self.request.GET.get("page", 1)
            search_results, _ = search_denials(
                request=self.request,
                search=search,
                filter=filter,
                page=page,
            )
            total_pages = search_results["total_pages"]
            count = search_results["count"]
            results = search_results["results"]

        ctx.update(
            {
                "case": self.case,
                "results": results,
                "count": count,
                "total_pages": total_pages,
                "parties": self.parties_to_search,
            }
        )

        return ctx
