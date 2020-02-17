from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.goods_types import goods_type_form
from applications.helpers.get_application_edit_type import get_application_edit_type, ApplicationEditTypes
from applications.services import (
    delete_goods_type,
    post_goods_type,
    put_goods_type_countries,
    get_application_goods_types,
    get_application_countries,
    get_application,
)
from lite_forms.generators import error_page
from lite_forms.views import SingleFormView


class GoodsTypeList(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        goods = get_application_goods_types(request, application_id)

        if not application["goods_types"]:
            return redirect(reverse_lazy("applications:add_goods_type", kwargs={"pk": application_id}))

        context = {
            "goods": goods,
            "application": application,
        }
        return render(request, "applications/goods-types/index.html", context)


class GoodsTypeAdd(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(request, self.object_pk)
        self.form = goods_type_form(application["case_type"]["sub_type"]["key"])
        self.action = post_goods_type
        self.success_url = reverse_lazy("applications:goods_types", kwargs={"pk": self.object_pk})


class GoodsTypeRemove(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        good_type_id = str(kwargs["goods_type_pk"])

        status_code = delete_goods_type(request, application_id, good_type_id)

        if status_code != 200:
            return error_page(request, "Unexpected error removing product description")

        return redirect(reverse_lazy("applications:goods_types", kwargs={"pk": application_id}))


class GoodsTypeCountries(TemplateView):
    """
    View to control which goods are going to which countries (goods/countries matrix)
    """

    application_id = None
    application = None
    goods = None
    countries = None

    def dispatch(self, request, *args, **kwargs):
        self.application_id = str(kwargs["pk"])
        self.application = get_application(request, self.application_id)
        self.goods = get_application_goods_types(request, self.application_id)
        self.countries = get_application_countries(request, self.application_id)

        # Prevent minor edits from accessing this page
        if get_application_edit_type(self.application) == ApplicationEditTypes.MINOR_EDIT:
            raise Http404

        return super(GoodsTypeCountries, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "countries": self.countries,
            "goods": self.goods,
            "draft_id": self.application_id,
            "select": request.GET.get("all", None),
        }
        return render(request, "applications/goods-types/countries.html", context)

    def post(self, request, **kwargs):
        data = request.POST.copy()
        data.pop("csrfmiddlewaretoken")

        post_data = {}

        for good_country in data:
            split_data = good_country.split(".")
            if str(split_data[0]) not in str(post_data):
                post_data[split_data[0]] = []
            post_data[split_data[0]].append(split_data[1])

        for good in self.goods:
            if good["id"] not in str(data):
                post_data[good["id"]] = []

        data, _ = put_goods_type_countries(request, self.application_id, post_data)

        if "errors" in data:
            # Merge post data and existing goods
            for good in self.goods:
                good["countries"] = [{"id": x} for x in post_data[good["id"]]]

            context = {
                "countries": self.countries,
                "goods": self.goods,
                "draft_id": self.application_id,
                "select": request.GET.get("all", None),
                "errors": data["errors"],
            }
            return render(request, "applications/goods-types/countries.html", context)

        return redirect(reverse_lazy("applications:task_list", kwargs={"pk": self.application_id}))
