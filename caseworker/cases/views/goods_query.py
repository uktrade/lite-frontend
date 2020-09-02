from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from caseworker.cases.forms.respond_to_good_query import respond_to_clc_query_form, respond_to_grading_query_form
from caseworker.cases.services import get_case, put_goods_query_clc, put_goods_query_pv_grading
from caseworker.core.constants import Permission
from caseworker.core.helpers import has_permission
from lite_content.lite_internal_frontend.cases import CLCReviewGoods, PVGradingForm
from lite_forms.views import SingleFormView

from core.auth.views import LoginRequiredMixin


class RespondCLCQuery(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.context = {"case": case}
        self.form = respond_to_clc_query_form(request, kwargs["queue_pk"], case)
        self.action = put_goods_query_clc
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.success_message = CLCReviewGoods.SUCCESS_MESSAGE

        if not has_permission(request, Permission.REVIEW_GOODS):
            return redirect(reverse_lazy("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk}))


class RespondPVGradingQuery(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        case = get_case(request, self.object_pk)
        self.context = {"case": case}
        self.form = respond_to_grading_query_form(request, kwargs["queue_pk"], case)
        self.action = put_goods_query_pv_grading
        self.success_url = reverse("cases:case", kwargs=kwargs)
        self.success_message = PVGradingForm.SUCCESS_MESSAGE

        if not has_permission(request, Permission.RESPOND_PV_GRADING):
            return redirect(reverse_lazy("cases:case", kwargs={"queue_pk": kwargs["queue_pk"], "pk": self.object_pk}))
