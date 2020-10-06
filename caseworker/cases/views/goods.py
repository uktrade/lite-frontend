from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from caseworker.cases.forms.review_goods import review_goods_form
from caseworker.cases.helpers.advice import get_param_goods, flatten_goods_data
from caseworker.cases.services import get_case, post_review_goods, get_good_on_application
from caseworker.search.services import get_search_results
from caseworker.search.forms import CasesSearchForm
from caseworker.core.constants import Permission
from caseworker.core.helpers import has_permission
from caseworker.core.services import get_control_list_entries
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class ReviewGoods(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        case_url = reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": kwargs["pk"]})
        if not has_permission(request, Permission.REVIEW_GOODS):
            return redirect(case_url)
        self.object_pk = kwargs["pk"]

        case = get_case(request, self.object_pk)
        param_goods = get_param_goods(request, case)
        control_list_entries = get_control_list_entries(request, convert_to_options=True)

        self.data = flatten_goods_data(param_goods)
        self.form = review_goods_form(control_list_entries=control_list_entries, back_url=case_url)
        self.context = {"case": case, "goods": param_goods}
        self.action = post_review_goods
        self.success_url = case_url


from django.utils.functional import cached_property


class GoodDetails(LoginRequiredMixin, FormView):
    template_name = "case/product-on-case.html"
    form_class = CasesSearchForm

    @cached_property
    def good_on_application(self):
        return get_good_on_application(self.request, pk=self.kwargs["good_pk"])

    def get_initial(self):
        part_number = self.good_on_application["good"]["part_number"]
        search_string = f'part:"{part_number}"'

        for item in self.good_on_application["control_list_entries"]:
            search_string += f' clc_rating: "{item["rating"]}"'

        return {"search_string": search_string}

    def get_context_data(self, **kwargs):
        case = get_case(self.request, self.kwargs["pk"])
        part_number = self.good_on_application["good"]["part_number"]
        other_cases = get_search_results(self.request, query_params={"part": part_number})
        return super().get_context_data(
            good_on_application=self.good_on_application,
            other_cases=other_cases,
            case=case,
            data={"total_pages": other_cases["count"] // self.get_form().page_size},  # for pagination
            **kwargs,
        )
