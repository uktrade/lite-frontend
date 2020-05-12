from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from cases.forms.review_goods import review_goods_form
from cases.services import get_case, post_review_goods
from cases.helpers.advice import get_param_goods
from conf.constants import Permission
from core.helpers import has_permission
from lite_forms.views import SingleFormView


class ReviewGoods(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.form = review_goods_form(request, is_goods_type="goods_types" in request.GET, **kwargs)
        self.context = {"case": case, "goods": get_param_goods(request, case)}
        self.action = post_review_goods
        self.success_url = reverse("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk})

        if not has_permission(request, Permission.REVIEW_GOODS):
            return redirect(reverse_lazy("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk}))
