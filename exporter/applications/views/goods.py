from http import HTTPStatus

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from s3chunkuploader.file_handler import S3FileUploadHandler

from exporter.applications.forms.goods import good_on_application_form_group
from exporter.applications.helpers.check_your_answers import get_total_goods_value
from exporter.applications.services import (
    get_application,
    get_application_goods,
    post_good_on_application,
    delete_application_preexisting_good,
    add_document_data,
    validate_good_on_application,
)
from exporter.core.constants import EXHIBITION, APPLICANT_EDITING
from core.helpers import convert_dict_to_query_params
from exporter.core.helpers import str_to_bool
from exporter.goods.forms import (
    document_grading_form,
    attach_documents_form,
    add_good_form_group,
)
from exporter.goods.services import (
    get_goods,
    get_good,
    post_goods,
    post_good_documents,
    post_good_document_sensitivity,
    validate_good,
)
from lite_forms.components import FiltersBar, TextInput
from exporter.goods.helpers import FIREARM_AMMUNITION_COMPONENT_TYPES
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView, MultiFormView

from core.auth.views import LoginRequiredMixin


class ApplicationGoodsList(LoginRequiredMixin, TemplateView):

    template_name = "applications/goods/index.html"

    def get_context_data(self, **kwargs):
        application = get_application(self.request, kwargs["pk"])
        goods = get_application_goods(self.request, kwargs["pk"])
        includes_firearms = any(["firearm_details" in good.keys() for good in goods])
        is_exhibition = application["case_type"]["sub_type"]["key"] == EXHIBITION
        return super().get_context_data(
            goods=goods,
            application=application,
            exhibition=is_exhibition,
            goods_value=None if is_exhibition else get_total_goods_value(goods),
            includes_firearms=includes_firearms,
            **kwargs,
        )


class ExistingGoodsList(LoginRequiredMixin, TemplateView):
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
            "feature_flag_firearms_enabled": settings.FEATURE_FLAG_FIREARMS_ENABLED,
        }
        return render(request, "applications/goods/preexisting.html", context)


class AddGood(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.draft_pk = str(kwargs["pk"])
        self.forms = add_good_form_group(request, draft_pk=self.draft_pk)
        self.action = validate_good

    def on_submission(self, request, **kwargs):
        copied_request = request.POST.copy()
        is_pv_graded = copied_request.get("is_pv_graded", "") == "yes"
        is_software_technology = copied_request.get("item_category") in ["group3_software", "group3_technology"]
        is_firearm = copied_request.get("type") == "firearms"
        is_firearms_core = copied_request.get("type") in FIREARM_AMMUNITION_COMPONENT_TYPES
        is_firearms_accessory = copied_request.get("type") == "firearms_accessory"
        is_firearms_software_tech = copied_request.get("type") in [
            "software_related_to_firearms",
            "technology_related_to_firearms",
        ]
        self.forms = add_good_form_group(
            request,
            is_pv_graded,
            is_software_technology,
            is_firearm,
            is_firearms_core,
            is_firearms_accessory,
            is_firearms_software_tech,
            draft_pk=self.draft_pk,
            base_form_back_link=reverse("applications:goods", kwargs={"pk": self.kwargs["pk"]}),
        )

        # we require the form index of the last form in the group, not the total number
        number_of_forms = len(self.forms.get_forms()) - 1

        if int(self.request.POST.get("form_pk")) == number_of_forms:
            self.action = post_goods

    def get_success_url(self):
        return reverse_lazy(
            "applications:add_good_summary",
            kwargs={"pk": self.draft_pk, "good_pk": self.get_validated_data()["good"]["id"]},
        )


class CheckDocumentGrading(LoginRequiredMixin, SingleFormView):
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
        return (
            reverse_lazy(url, kwargs={"pk": self.draft_pk, "good_pk": self.object_pk})
            + f"?preexisting={self.request.GET.get('preexisting', False)}"
        )


@method_decorator(csrf_exempt, "dispatch")
class AttachDocument(LoginRequiredMixin, TemplateView):
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
            + f"?preexisting={self.request.GET.get('preexisting', False)}"
        )


class AddGoodToApplication(LoginRequiredMixin, MultiFormView):
    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        good_pk = kwargs["good_pk"]
        application = get_application(self.request, self.object_pk)
        good, _ = get_good(request, good_pk)

        sub_case_type = application["case_type"]["sub_type"]
        is_preexisting = str_to_bool(request.GET.get("preexisting", True))

        self.forms = good_on_application_form_group(
            request, is_preexisting=is_preexisting, good=good, sub_case_type=sub_case_type, draft_pk=self.object_pk
        )

        self.action = validate_good_on_application
        self.success_url = reverse_lazy("applications:goods", kwargs={"pk": self.object_pk})

    def on_submission(self, request, **kwargs):
        # we require the form index of the last form in the group, not the total number

        number_of_forms = len(self.forms.get_forms()) - 1
        if int(self.request.POST.get("form_pk")) == number_of_forms:
            self.action = post_good_on_application


class RemovePreexistingGood(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        good_on_application_id = str(kwargs["good_on_application_pk"])

        status_code = delete_application_preexisting_good(request, good_on_application_id)

        if status_code != 200:
            return error_page(request, "Unexpected error removing product")

        return redirect(reverse_lazy("applications:goods", kwargs={"pk": application_id}))


class GoodsDetailSummaryCheckYourAnswers(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)

        context = {
            "application_id": application_id,
            "goods": application["goods"],
            "application_status_draft": application["status"]["key"] in ["draft", APPLICANT_EDITING],
        }
        return render(request, "applications/goods/goods-detail-summary.html", context)


class AddGoodsSummary(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        good_id = str(kwargs["good_pk"])
        good = get_good(request, good_id, full_detail=True)[0]

        context = {"good": good, "application_id": application_id, "good_id": good_id}

        return render(request, "applications/goods/add-good-detail-summary.html", context)
