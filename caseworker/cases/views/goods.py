from caseworker.cases.forms.review_goods import review_goods_form
from caseworker.cases.helpers.advice import get_param_goods, flatten_goods_data
from caseworker.cases.services import get_case, post_review_goods, get_good_on_application
from caseworker.search.services import get_search_results
from caseworker.search.forms import CasesSearchForm
from caseworker.core.constants import Permission
from caseworker.core.helpers import has_permission
from caseworker.core.services import get_control_list_entries
from lite_forms.views import SingleFormView

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView
from django.utils.functional import cached_property

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


class GoodDetails(LoginRequiredMixin, FormView):
    template_name = "case/product-on-case.html"
    form_class = CasesSearchForm

    @cached_property
    def object(self):
        return get_good_on_application(self.request, pk=self.kwargs["good_pk"])

    @cached_property
    def other_cases(self):
        form = self.get_form()
        search_string = self.get_initial()["search_string"]
        if search_string:
            return get_search_results(self.request, query_params=form.extract_filters(search_string))
        return []

    def get_initial(self):
        search_string = ""
        part_number = self.object["good"]["part_number"]
        if part_number:
            search_string += f'part:"{part_number}"'
        control_list_entries = self.object["control_list_entries"] or self.object["good"]["control_list_entries"]
        for item in control_list_entries:
            search_string += f' clc_rating:"{item["rating"]}"'
        return {"search_string": search_string.strip()}

    def get_context_data(self, **kwargs):
        form = self.get_form()
        return super().get_context_data(
            good_on_application=self.object,
            case=get_case(self.request, self.kwargs["pk"]),
            other_cases=self.other_cases,
            # for pagination
            data={"total_pages": self.other_cases["count"] // form.page_size} if self.other_cases else {},
            **kwargs,
        )
