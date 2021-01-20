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
    post_application_document,
    delete_application_document_data,
    get_application_documents,
    get_application_document,
    download_document_from_s3,
)
from exporter.core.constants import EXHIBITION, APPLICANT_EDITING, FIREARM_AMMUNITION_COMPONENT_TYPES
from core.helpers import convert_dict_to_query_params
from exporter.core.helpers import str_to_bool
from exporter.goods.forms import (
    document_grading_form,
    attach_documents_form,
    add_good_form_group,
    upload_firearms_act_certificate_form,
    build_firearm_back_link_create,
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
        name = request.GET.get("name", "").strip()
        description = request.GET.get("description", "").strip()
        part_number = request.GET.get("part_number", "").strip()
        control_list_entry = request.GET.get("control_list_entry", "").strip()

        filters = FiltersBar(
            [
                TextInput(title="name", name="name"),
                TextInput(title="description", name="description"),
                TextInput(title="control list entry", name="control_list_entry"),
                TextInput(title="part number", name="part_number"),
            ]
        )

        params = {
            "page": int(request.GET.get("page", 1)),
            "name": name,
            "description": description,
            "part_number": part_number,
            "control_list_entry": control_list_entry,
            "for_application": "True",
        }
        goods_list = get_goods(request, **params)

        context = {
            "application": application,
            "data": goods_list,
            "name": name,
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
        self.show_section_upload_form = False

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

        firearm_act_status = copied_request.get("is_covered_by_firearm_act_section_one_two_or_five", "")
        selected_section = copied_request.get("firearms_act_section", "")

        self.covered_by_firearms_act = firearm_act_status == "Yes"
        self.certificate_not_required = firearm_act_status == "No" or firearm_act_status == "Unsure"
        self.show_section_upload_form = self.covered_by_firearms_act and (
            selected_section == "firearms_act_section1" or selected_section == "firearms_act_section2"
        )

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
            if self.show_section_upload_form:
                firearms_data_id = f"post_{request.session['lite_api_user_id']}_{self.draft_pk}"
                session_data = copied_request.dict()
                if "control_list_entries[]" in copied_request:
                    session_data["control_list_entries"] = copied_request.getlist("control_list_entries[]")
                    del session_data["control_list_entries[]"]

                request.session[firearms_data_id] = session_data

            elif self.certificate_not_required:
                self.action = post_goods
            else:
                self.action = post_goods

    def get_success_url(self):
        if self.show_section_upload_form:
            return reverse_lazy("applications:attach-firearms-certificate", kwargs={"pk": self.kwargs["pk"]})
        else:
            good = self.get_validated_data()["good"]
            return reverse_lazy(
                "applications:add_good_summary", kwargs={"pk": self.kwargs["pk"], "good_pk": good["id"]}
            )


@method_decorator(csrf_exempt, "dispatch")
class AttachFirearmActSectionDocument(LoginRequiredMixin, TemplateView):
    def dispatch(self, request, **kwargs):
        self.draft_pk = str(kwargs["pk"])
        self.good_pk = str(kwargs.get("good_pk", ""))
        if self.good_pk:
            self.firearms_data_id = f"post_{request.session['lite_api_user_id']}_{self.draft_pk}_{self.good_pk}"
        else:
            self.firearms_data_id = f"post_{request.session['lite_api_user_id']}_{self.draft_pk}"

        self.selected_section = "section"
        self.certificate_filename = ""
        post_data = request.session[self.firearms_data_id]

        if post_data["firearms_act_section"] == "firearms_act_section1":
            self.selected_section = "Section 1"
        elif post_data["firearms_act_section"] == "firearms_act_section2":
            self.selected_section = "Section 2"

        return super().dispatch(request, **kwargs)

    def get(self, request, **kwargs):
        back_link = build_firearm_back_link_create(
            form_url=reverse("applications:new_good", kwargs={"pk": kwargs["pk"]}),
            form_data=request.session.get(self.firearms_data_id, {}),
        )
        form = upload_firearms_act_certificate_form(section=self.selected_section, filename="", back_link=back_link)
        return form_page(request, form)

    @csrf_exempt
    def post(self, request, **kwargs):
        self.request.upload_handlers.insert(0, S3FileUploadHandler(request))
        certificate_available = request.POST.get("section_certificate_missing", False) is False

        doc_data = {}
        doc_error = None
        new_file_selected = False
        file_upload_key = f"{self.firearms_data_id}_file"

        doc_data, doc_error = add_document_data(request)
        if doc_data:
            request.session[file_upload_key] = doc_data
            self.certificate_filename = doc_data["name"]
            new_file_selected = True
        else:
            file_info = request.session.get(file_upload_key)
            if file_info:
                doc_data = file_info
                doc_error = None
                new_file_selected = True
                self.certificate_filename = file_info["name"]

        old_post = request.session.get(self.firearms_data_id, None)
        if not old_post:
            return error_page(request, "Firearms data from previous forms is missing in session")

        copied_request = {k: request.POST.get(k) for k in request.POST}
        data = {**old_post, **copied_request}
        back_link = build_firearm_back_link_create(
            form_url=reverse("applications:new_good", kwargs={"pk": kwargs["pk"]}), form_data=old_post,
        )

        if self.good_pk:
            response, status_code = post_good_on_application(request, self.draft_pk, data)
            if status_code != HTTPStatus.CREATED:
                if doc_error:
                    response["errors"]["file"] = ["Select certificate file to upload"]
                form = upload_firearms_act_certificate_form(
                    section="section", filename=self.certificate_filename, back_link=back_link,
                )
                return form_page(request, form, data=data, errors=response["errors"])

            success_url = reverse_lazy("applications:goods", kwargs={"pk": self.draft_pk})

        else:
            response, status_code = post_goods(request, data)
            if status_code != HTTPStatus.CREATED:
                if doc_error:
                    response["errors"]["file"] = ["Select certificate file to upload"]
                form = upload_firearms_act_certificate_form(
                    section="section", filename=self.certificate_filename, back_link=back_link,
                )
                return form_page(request, form, data=data, errors=response["errors"])

            self.good_pk = response["good"]["id"]
            success_url = reverse(
                "applications:add_good_summary", kwargs={"pk": self.draft_pk, "good_pk": self.good_pk}
            )

        if certificate_available and new_file_selected:
            data, status_code = post_application_document(request, self.draft_pk, self.good_pk, doc_data)
            if status_code != HTTPStatus.CREATED:
                return error_page(request, data["errors"]["file"])
        elif doc_data:
            delete_application_document_data(request, self.draft_pk, self.good_pk, doc_data)

        self.certificate_filename = ""
        del request.session[self.firearms_data_id]
        del request.session[file_upload_key]
        request.session.modified = True

        return redirect(success_url)


class CheckDocumentGrading(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.draft_pk = kwargs["pk"]
        self.object_pk = kwargs["good_pk"]
        back_link = reverse("applications:add_good_summary", kwargs={"pk": self.draft_pk, "good_pk": self.object_pk})
        self.form = document_grading_form(request, self.object_pk, back_url=back_link)
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
        self.good_pk = kwargs["good_pk"]
        application = get_application(self.request, self.object_pk)
        good, _ = get_good(request, self.good_pk)

        sub_case_type = application["case_type"]["sub_type"]
        is_preexisting = str_to_bool(request.GET.get("preexisting", True))

        self.forms = good_on_application_form_group(
            request, is_preexisting=is_preexisting, good=good, sub_case_type=sub_case_type, draft_pk=self.object_pk
        )

        self.action = validate_good_on_application
        self.success_url = reverse_lazy(
            "applications:attach-firearms-certificate-existing-good",
            kwargs={"pk": self.object_pk, "good_pk": self.good_pk},
        )

    def on_submission(self, request, **kwargs):
        selected_section = request.POST.get("firearms_act_section")
        show_section_upload_form = request.POST.get("is_covered_by_firearm_act_section_one_two_or_five", False) and (
            selected_section == "firearms_act_section1" or selected_section == "firearms_act_section2"
        )
        # we require the form index of the last form in the group, not the total number
        number_of_forms = len(self.forms.get_forms()) - 1
        if int(self.request.POST.get("form_pk")) == number_of_forms:
            if show_section_upload_form:
                firearms_data_id = f"post_{request.session['lite_api_user_id']}_{self.object_pk}_{self.good_pk}"
                request.session[firearms_data_id] = self.request.POST.copy()
            else:
                self.action = post_good_on_application
                self.success_url = reverse("applications:goods", kwargs={"pk": self.object_pk})


class GoodOnApplicationDocumentView(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        pk = str(kwargs["pk"])
        good_pk = str(kwargs["good_pk"])
        doc_pk = str(kwargs["doc_pk"])

        document, _ = get_application_document(request, pk, good_pk, doc_pk)
        return download_document_from_s3(document["s3_key"], document["name"])


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

        good_application_documents, status = get_application_documents(request, application_id, good_id)  # noqa

        context = {
            "good": good,
            "application_id": application_id,
            "good_id": good_id,
            "good_application_documents": good_application_documents["documents"],
        }

        return render(request, "applications/goods/add-good-detail-summary.html", context)
