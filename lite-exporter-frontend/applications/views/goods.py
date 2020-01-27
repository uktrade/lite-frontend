from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler

from applications.forms.goods import good_on_application_form
from applications.helpers.check_your_answers import get_total_goods_value
from applications.services import (
    get_application,
    get_application_goods,
    get_application_goods_types,
    post_good_on_application,
    delete_application_preexisting_good,
    add_document_data,
)
from core.helpers import convert_dict_to_query_params
from core.services import get_units

from goods.forms import document_grading_form, attach_documents_form, add_good_form_group
from goods.services import (
    get_goods,
    get_good,
    post_goods,
    post_good_documents,
    post_good_document_sensitivity,
    validate_good,
    post_good_with_pv_grading,
)
from lite_content.lite_exporter_frontend import strings
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView, MultiFormView


class DraftGoodsList(TemplateView):
    def get(self, request, **kwargs):
        """
        List all goods relating to the draft
        """
        draft_id = str(kwargs["pk"])
        application = get_application(request, draft_id)
        goods = get_application_goods(request, draft_id)
        goods_value = get_total_goods_value(goods)

        context = {"goods": goods, "application": application, "goods_value": goods_value}
        return render(request, "applications/goods/index.html", context)


class GoodsList(TemplateView):
    def get(self, request, **kwargs):
        """
        List of existing goods  (add-preexisting)
        """
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        description = request.GET.get("description", "").strip()
        part_number = request.GET.get("part_number", "").strip()
        control_rating = request.GET.get("control_rating", "").strip()

        params = {
            "page": int(request.GET.get("page", 1)),
            "description": description,
            "part_number": part_number,
            "control_rating": control_rating,
            "for_application": "True",
        }
        goods_list = get_goods(request, **params)

        context = {
            "application": application,
            "data": goods_list,
            "description": description,
            "part_number": part_number,
            "control_code": control_rating,
            "draft_id": application_id,
            "params": params,
            "page": params.pop("page"),
            "params_str": convert_dict_to_query_params(params),
        }
        return render(request, "applications/goods/preexisting.html", context)


class AddGood(MultiFormView):
    actions = [validate_good, post_goods, post_good_with_pv_grading]

    def init(self, request, **kwargs):
        self.draft_pk = str(kwargs["pk"])
        self.forms = add_good_form_group(draft_pk=self.draft_pk)
        self.action = post_goods

    def on_submission(self, request, **kwargs):
        self.draft_pk = str(kwargs["pk"])
        is_pv_graded = request.POST.copy().get("is_pv_graded", "").lower() == "yes"
        self.forms = add_good_form_group(is_pv_graded, draft_pk=self.draft_pk)
        if int(self.request.POST.get("form_pk")) == 1:
            self.action = self.actions[2]
        elif (int(self.request.POST.get("form_pk")) == 0) and is_pv_graded:
            self.action = self.actions[0]

    def get_success_url(self):
        return reverse_lazy(
            "applications:add_document",
            kwargs={"pk": self.draft_pk, "good_pk": self.get_validated_data()["good"]["id"]},
        )


class CheckDocumentGrading(SingleFormView):
    def init(self, request, **kwargs):
        self.draft_pk = kwargs["pk"]
        self.object_pk = kwargs["good_pk"]
        self.form = document_grading_form(request, self.object_pk)
        self.action = post_good_document_sensitivity

    def get_success_url(self):
        good = self.get_validated_data()["good"]
        if good["missing_document_reason"]:
            url = "applications:add_good_to_application"
        else:
            url = "applications:attach_documents"
        return reverse_lazy(url, kwargs={"pk": self.draft_pk, "good_pk": self.object_pk})


@method_decorator(csrf_exempt, "dispatch")
class AttachDocument(TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["good_pk"])
        draft_id = str(kwargs["pk"])
        back_link = reverse_lazy("applications:add_good_to_application", kwargs={"pk": draft_id, "good_pk": good_id})
        form = attach_documents_form(back_link)
        return form_page(request, form, extra_data={"good_id": good_id})

    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))

        good_id = str(kwargs["good_pk"])
        draft_id = str(kwargs["pk"])
        data, error = add_document_data(request)

        if error:
            return error_page(request, error)

        if "errors" in post_good_documents(request, good_id, data):
            return error_page(request, strings.goods.AttachDocumentPage.UPLOAD_FAILURE_ERROR)

        return redirect(
            reverse_lazy("applications:add_good_to_application", kwargs={"pk": draft_id, "good_pk": good_id})
        )


class DraftOpenGoodsTypeList(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        goods = get_application_goods_types(request, application_id)

        context = {
            "goods": goods,
            "application": application,
        }
        return render(request, "applications/goodstype/index.html", context)


class AddGoodToApplication(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        good, _ = get_good(request, kwargs["good_pk"])
        self.form = good_on_application_form(good, get_units(request))
        self.action = post_good_on_application
        self.success_url = reverse_lazy("applications:goods", kwargs={"pk": self.object_pk})


class RemovePreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        good_on_application_id = str(kwargs["good_on_application_pk"])

        status_code = delete_application_preexisting_good(request, good_on_application_id)

        if status_code != 200:
            return error_page(request, "Unexpected error removing good")

        return redirect(reverse_lazy("applications:goods", kwargs={"pk": application_id}))
