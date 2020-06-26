from http import HTTPStatus

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
    post_good_on_application,
    delete_application_preexisting_good,
    add_document_data,
)
from conf.constants import EXHIBITION, APPLICANT_EDITING
from core.helpers import convert_dict_to_query_params
from goods.forms import (
    document_grading_form,
    attach_documents_form,
    add_good_form_group,
)
from goods.services import (
    get_goods,
    get_good,
    post_goods,
    post_good_documents,
    post_good_document_sensitivity,
    validate_good,
)
from lite_forms.components import FiltersBar, TextInput
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView, MultiFormView


class ApplicationGoodsList(TemplateView):
    def get(self, request, **kwargs):
        """
        List all goods relating to the application
        """
        draft_id = str(kwargs["pk"])
        application = get_application(request, draft_id)
        goods = get_application_goods(request, draft_id)
        exhibition = application["case_type"]["sub_type"]["key"] == EXHIBITION

        context = {"goods": goods, "application": application, "exhibition": exhibition}
        if not exhibition:
            context["goods_value"] = get_total_goods_value(goods)
        return render(request, "applications/goods/index.html", context)


class ExistingGoodsList(TemplateView):
    def get(self, request, **kwargs):
        """
        List of existing goods (add-preexisting)
        """
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        description = request.GET.get("description", "").strip()
        part_number = request.GET.get("part_number", "").strip()
        control_list_entry = request.GET.get("control_list_entry", "").strip()

        filters = FiltersBar(
            [
                TextInput(title="description", name="description"),
                TextInput(title="control list entry", name="control_list_entry"),
                TextInput(title="part number", name="part_number"),
            ]
        )

        params = {
            "page": int(request.GET.get("page", 1)),
            "description": description,
            "part_number": part_number,
            "control_list_entry": control_list_entry,
            "for_application": "True",
        }
        goods_list = get_goods(request, **params)

        context = {
            "application": application,
            "data": goods_list,
            "description": description,
            "part_number": part_number,
            "control_list_entry": control_list_entry,
            "draft_id": application_id,
            "params": params,
            "page": params.pop("page"),
            "params_str": convert_dict_to_query_params(params),
            "filters": filters,
        }
        return render(request, "applications/goods/preexisting.html", context)


class AddGood(MultiFormView):
    def init(self, request, **kwargs):
        self.draft_pk = str(kwargs["pk"])
        self.forms = add_good_form_group(request, draft_pk=self.draft_pk)
        self.action = validate_good

    def on_submission(self, request, **kwargs):
        copied_request = request.POST.copy()
        is_pv_graded = copied_request.get("is_pv_graded", "") == "yes"
        is_software_technology = copied_request.get("item_category") in ["group3_software", "group3_technology"]
        self.forms = add_good_form_group(request, is_pv_graded, is_software_technology, draft_pk=self.draft_pk)

        if is_pv_graded:
            # post on step 5 in both software/technology and group 1
            if int(self.request.POST.get("form_pk")) == 5:
                self.action = post_goods
        else:
            # post on step 4 in both software/technology and group 1
            if int(self.request.POST.get("form_pk")) == 4:
                self.action = post_goods

    def get_success_url(self):
        return reverse_lazy(
            "applications:add_good_summary",
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

        data, status_code = post_good_documents(request, good_id, data)
        if status_code != HTTPStatus.CREATED:
            return error_page(request, data["errors"]["file"])

        return redirect(
            reverse_lazy("applications:add_good_to_application", kwargs={"pk": draft_id, "good_pk": good_id})
        )


class AddGoodToApplication(SingleFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        application = get_application(self.request, self.object_pk)
        good, _ = get_good(request, kwargs["good_pk"])
        self.form = good_on_application_form(request, good, application["case_type"]["sub_type"], self.object_pk)
        self.action = post_good_on_application
        self.success_url = reverse_lazy("applications:goods", kwargs={"pk": self.object_pk})


class RemovePreexistingGood(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        good_on_application_id = str(kwargs["good_on_application_pk"])

        status_code = delete_application_preexisting_good(request, good_on_application_id)

        if status_code != 200:
            return error_page(request, "Unexpected error removing product")

        return redirect(reverse_lazy("applications:goods", kwargs={"pk": application_id}))


class GoodsDetailSummaryCheckYourAnswers(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        context = {
            "application_id": application_id,
            "goods": application["goods"],
            "application_status_draft": application["status"]["key"] in ["draft", APPLICANT_EDITING],
        }
        return render(request, "applications/goods/goods-detail-summary.html", context)


class AddGoodsSummary(TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        good_id = str(kwargs["good_pk"])
        good = get_good(request, good_id, full_detail=True)[0]

        context = {"good": good, "application_id": application_id, "good_id": good_id}

        return render(request, "applications/goods/add-good-detail-summary.html", context)
