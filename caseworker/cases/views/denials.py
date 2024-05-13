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
    reg_expression_search_query = re.compile('[a-z_]+?:".*?"')

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

    def get_search_filter(self):

        search_filter = []
        filter = {
            "country": set(),
        }

        for party in self.parties_to_search:
            search_filter.append(f'name:"{party["name"]}"')
            search_filter.append(f'address:"{party["address"]}"')
            filter["country"].add(party["country"]["name"])
        return (" ".join(search_filter), filter)

    def get_initial(self):

        default_search, _ = self.get_search_filter()
        return {
            "search_string": default_search,
        }

    def form_valid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        total_pages = 0
        count = 0
        results = []
        search = []

        search_string, filter = self.get_search_filter()

        if self.request.method == "POST":
            search_string = kwargs["form"].cleaned_data["search_string"]

        search_string = self.reg_expression_search_query.findall(search_string)
        search = [s.replace('"', "") for s in search_string]

        if search:
            search_results, _ = search_denials(request=self.request, search=search, filter=filter)
            results = search_results["results"]
            total_pages = search_results["total_pages"]
            count = search_results["count"]

        return super().get_context_data(
            search_string=search,
            case=self.case,
            results=results,
            count=count,
            total_pages=total_pages,
            parties=self.parties_to_search,
            **kwargs,
        )
