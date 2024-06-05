import re
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        _, session_countries_list, _ = self.get_search_params_from_session()
        _, country_list = self.get_search_params()

        kwargs["countries"] = session_countries_list or country_list
        return kwargs

    def get_initial(self):
        session_search_string, _, session_selected_countries = self.get_search_params_from_session()
        default_search_string, default_country_list = self.get_search_params()

        return {
            "search_string": session_search_string or default_search_string,
            "country_filter": session_selected_countries or default_country_list,
        }

    def form_valid(self, form):
        search_id = self.request.GET.get("search_id", 1)
        countries_list = set(c[0] for c in form.fields["country_filter"].choices)
        search_string = form.cleaned_data["search_string"]
        selected_countries = form.cleaned_data["country_filter"]

        self.request.session["search_params"] = {search_id: (search_string, countries_list, selected_countries)}
        return self.render_to_response(self.get_context_data(form=form))

    def get_search_params_from_session(self):
        # This is required since the search_string shouldn't be sent in the query string due to sensative data
        # so we require a search_string to be sent via post. Since the pagination currently works as a get only
        # the query_string set by the user gets lost we should aim to move away from sessions once we have
        # pagination that works with a post
        search_id = self.request.GET.get("search_id", 1)

        if self.request.session.get("search_params") and self.request.session.get("search_params").get(search_id):
            return self.request.session["search_params"][search_id]
        # We store a tuble of 3 values if nothing is found return all 3 as None.
        return (None, None, None)

    def get_context_data(self, **kwargs):
        total_pages = 0
        search_results = []

        default_search_string, country_list = self.get_search_params()

        session_search_string, _, session_selected_countries = self.get_search_params_from_session()
        search = session_search_string or default_search_string
        country_filter = country_list if session_selected_countries is None else session_selected_countries

        if search:
            filter = {
                "country": set(country_filter),
            }
            search_results, _ = search_denials(request=self.request, search=search, filter=filter)
            total_pages = search_results.get("total_pages", 0)

        return super().get_context_data(
            search_string=search,
            case=self.case,
            total_pages=total_pages,
            search_results=search_results,
            parties=self.parties_to_search,
            **kwargs,
        )
