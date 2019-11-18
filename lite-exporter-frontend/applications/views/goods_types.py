from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from applications.forms.goods_types import goods_type_form
from applications.services import (
    delete_goods_type,
    post_goods_type,
    post_goods_type_countries,
    get_application_goods_types,
    get_application_countries,
    get_application,
)
from lite_forms.generators import form_page, error_page


class DraftOpenGoodsTypeList(TemplateView):
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
        return render(request, "applications/goods_types/index.html", context)


class ApplicationAddGoodsType(TemplateView):
    def get(self, request, **kwargs):
        return form_page(request, goods_type_form())

    def post(self, request, **kwargs):
        copied_post = request.POST.copy()
        data, status_code = post_goods_type(request, str(kwargs.get("pk")), copied_post)

        if status_code == 400:
            return form_page(request, goods_type_form(), request.POST, errors=data["errors"])

        return redirect(reverse_lazy("applications:goods_types", args=[kwargs["pk"]]))


class ApplicationRemoveGoodsType(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        good_type_id = str(kwargs["goods_type_pk"])

        status_code = delete_goods_type(request, application_id, good_type_id)

        if status_code != 200:
            return error_page(request, "Unexpected error removing goods description")

        return redirect(reverse_lazy("applications:goods_types", kwargs={"pk": application_id}))


class GoodsTypeCountries(TemplateView):
    goods = None
    countries = None
    draft_id = None

    def dispatch(self, request, *args, **kwargs):
        self.draft_id = str(kwargs["pk"])
        self.goods = get_application_goods_types(request, self.draft_id)
        self.countries = get_application_countries(request, self.draft_id)

        return super(GoodsTypeCountries, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "countries": self.countries,
            "goods": self.goods,
            "draft_id": self.draft_id,
            "select": request.GET.get("all", None),
        }
        return render(request, "applications/goods_types/countries.html", context)

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

        post_goods_type_countries(request, self.draft_id, list(post_data.keys())[0], post_data)

        return redirect(reverse_lazy("applications:task_list", kwargs={"pk": self.draft_id}))
