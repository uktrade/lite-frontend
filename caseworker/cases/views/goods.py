from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from caseworker.cases.forms.review_goods import review_goods_form
from caseworker.cases.helpers.advice import get_param_goods, flatten_goods_data
from caseworker.cases.services import get_case, post_review_goods, get_good
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


class GoodDetails(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["good_pk"])
        good = get_good(request, good_id)[0]["good"]
        return render(request, "case/popups/good.html", {"good": good})
