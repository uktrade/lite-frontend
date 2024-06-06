from django.conf import settings
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

    def get_search_params(self):
        """
        This is building the query_string that will be executed directly by the backend
        The field query is contained within () without this ES gets confused and searches
        across columns even when the column name is given.
        """
        search_filter = []
        country_list = set()

        for party in self.parties_to_search:
            search_filter.append(f'name:({party["name"]})')
            search_filter.append(f'address:({party["address"]})')
            country_list.add(party["country"]["name"])
        return (" ".join(search_filter), country_list)

    def get_form_action(self):
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

        return f"{form_action}?{query.urlencode()}"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        _, country_list = self.get_search_params()
        kwargs["countries"] = country_list

        kwargs["form_action"] = self.get_form_action()

        return kwargs

    def get_initial(self):
        search_string, selected_countries = self.get_search_params()

        return {
            "search_string": search_string,
            "country_filter": selected_countries,
        }

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        total_pages = 0
        search_results = []

        search, country_filter = self.get_search_params()

        if search:
            filter = {
                "country": set(country_filter),
            }
            search_results, _ = search_denials(request=self.request, search=search, filter=filter)
            total_pages = search_results.get("total_pages", 0)

        context = super().get_context_data(
            search_string=search,
            case=self.case,
            total_pages=total_pages,
            search_results=search_results,
            parties=self.parties_to_search,
            search_score_feature_flag=settings.FEATURE_FLAG_DENIALS_SEARCH_SCORE,
            **kwargs,
        )

        return context
