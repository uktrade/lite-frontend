from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView

from caseworker.cases.forms.review_goods import review_goods_form
from caseworker.cases.helpers.advice import get_param_goods, flatten_goods_data
from caseworker.cases.services import get_case, post_review_goods, get_good
from caseworker.core.constants import Permission
from caseworker.core.helpers import has_permission
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class ReviewGoods(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.data = flatten_goods_data(get_param_goods(request, case))
        self.form = review_goods_form(request, is_goods_type="goods_types" in request.GET, **kwargs)
        self.context = {"case": case, "goods": get_param_goods(request, case)}
        self.action = post_review_goods
        self.success_url = reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk})

        if not has_permission(request, Permission.REVIEW_GOODS):
            return redirect(reverse_lazy("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk}))


class GoodDetails(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["good_pk"])
        good = get_good(request, good_id)[0]["good"]
        return render(request, "case/popups/good.html", {"good": good})
