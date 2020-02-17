from lite_content.lite_internal_frontend.strings import cases
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from lite_forms.generators import form_page

from cases.constants import CaseType
from cases.forms.review_goods_clc import review_goods_clc_query_form
from cases.services import get_good, get_case, post_goods_control_code, get_goods_type
from core.helpers import convert_dict_to_query_params
from core.services import get_user_permissions


class ReviewGoods(TemplateView):
    def get(self, request, **kwargs):
        case_id = str(kwargs["pk"])

        action = request.GET.get("action")
        if action == "edit-flags":
            params = dict()
            params["goods"] = request.GET.getlist("goods")
            params["level"] = "goods"
            post_url = "?" + convert_dict_to_query_params(params)
            return redirect(reverse_lazy("cases:assign_flags", kwargs={"pk": case_id}) + post_url)

        permissions = get_user_permissions(request)
        if "REVIEW_GOODS" not in permissions:
            return redirect(reverse_lazy("cases:case", kwargs={"pk": case_id}))

        goods_pk_list = request.GET.getlist("items", request.GET.getlist("goods"))
        goods = []

        if not goods_pk_list:
            return redirect(reverse_lazy("cases:case", kwargs={"pk": case_id}))

        case = get_case(request, case_id)

        edit_flags_url = reverse_lazy("cases:assign_flags", kwargs={"pk": case_id})
        review_goods_clc_url = reverse_lazy("cases:review_goods_clc", kwargs={"pk": case_id})
        parameters = {"level": "goods", "origin": "review_goods", "goods": goods_pk_list}
        goods_postfix_url = "?" + convert_dict_to_query_params(parameters)

        if case["application"]["case_type"]["sub_type"]["key"] == "standard":
            for good in case["application"]["goods"]:
                if good["good"]["id"] in goods_pk_list:
                    # flatten the good details onto the first layer of the dictionary
                    # (so both good on app and good details are together)
                    flatten = good
                    for key, val in good["good"].items():
                        flatten[key] = val
                    goods.append(flatten)
        else:
            for good in case["application"]["goods_types"]:
                if good["id"] in goods_pk_list:
                    goods.append(good)

        context = {
            "title": cases.ReviewGoodsSummary.HEADING,
            "case_id": case_id,
            "case_sub_type": case["application"]["case_type"]["sub_type"]["key"],
            "objects": goods,
            "edit_flags_url": edit_flags_url + goods_postfix_url,
            "review_goods_clc_url": review_goods_clc_url + goods_postfix_url,
        }
        return render(request, "case/views/review-goods.html", context)


class ReviewGoodsClc(TemplateView):
    case_id = None
    goods = None
    back_link = None

    def dispatch(self, request, *args, **kwargs):
        self.case_id = str(kwargs["pk"])

        permissions = get_user_permissions(request)
        if "REVIEW_GOODS" not in permissions:
            return redirect(reverse_lazy("cases:case", kwargs={"pk": self.case_id}))

        self.goods = request.GET.getlist("items", request.GET.getlist("goods"))

        parameters = {"goods": self.goods}
        goods_postfix_url = "?" + convert_dict_to_query_params(parameters)

        self.back_link = reverse_lazy("cases:review_goods", kwargs={"pk": self.case_id}) + goods_postfix_url

        return super(ReviewGoodsClc, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        case = get_case(request, self.case_id)
        if case["application"]["case_type"]["sub_type"]["key"] == "standard":
            get_good_func = get_good
            form = review_goods_clc_query_form(request, self.back_link, is_goods_type=False)
        else:
            get_good_func = get_goods_type
            form = review_goods_clc_query_form(request, self.back_link, is_goods_type=True)

        if len(self.goods) == 1:
            data = get_good_func(request, self.goods[0])[0]["good"]
        else:
            initial_good = get_good_func(request, self.goods[0])[0]["good"]
            for good in self.goods[1:]:
                good_data = get_good_func(request, good)[0]["good"]
                if (
                    initial_good["control_code"] != good_data["control_code"]
                    or initial_good["is_good_controlled"] != good_data["is_good_controlled"]
                    or initial_good["comment"] != good_data["comment"]
                    or initial_good["report_summary"] != good_data["report_summary"]
                ):
                    return form_page(request, form)
            data = initial_good
        data["is_good_controlled"] = str(data["is_good_controlled"])
        return form_page(request, form, data=data)

    def post(self, request, *args, **kwargs):
        form_data = {
            "objects": self.goods,
            "comment": request.POST.get("comment"),
            "control_code": request.POST.get("control_code", None),
            "is_good_controlled": request.POST.get("is_good_controlled"),
        }

        report_summary = request.POST.get("report_summary", None)

        form_data["report_summary"] = report_summary if report_summary and report_summary != "None" else None

        response = post_goods_control_code(request, self.case_id, form_data)

        if response.status_code == 400:
            case = get_case(request, self.case_id)
            is_goods_type = case["application"]["case_type"]["sub_type"]["key"] != CaseType.STANDARD.value

            form = review_goods_clc_query_form(request, self.back_link, is_goods_type=is_goods_type)
            return form_page(request, form, data=request.POST, errors=response.json().get("errors"))

        return redirect(self.back_link)
