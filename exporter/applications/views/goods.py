import logging

from datetime import datetime
from http import HTTPStatus

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView

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
    post_additional_document,
    delete_application_document_data,
    get_application_documents,
    get_application_document,
    download_document_from_s3,
)
from exporter.core import constants
from exporter.core.helpers import get_firearms_subcategory
from core.helpers import convert_dict_to_query_params
from exporter.core.helpers import str_to_bool
from exporter.goods.forms import (
    check_document_available_form,
    document_grading_form,
    attach_documents_form,
    add_good_form_group,
    upload_firearms_act_certificate_form,
    build_firearm_back_link_create,
    has_valid_rfd_certificate,
    has_valid_section_five_certificate,
)
from exporter.goods.services import (
    get_goods,
    get_good,
    post_goods,
    post_good_documents,
    get_good_document_availability,
    post_good_document_availability,
    get_good_document_sensitivity,
    post_good_document_sensitivity,
    validate_good,
)

from exporter.applications.helpers.date_fields import format_date
from exporter.core.validators import validate_expiry_date
from lite_forms.components import FiltersBar, TextInput, BackLink
from lite_forms.generators import error_page, form_page
from lite_forms.helpers import get_form_by_pk
from lite_forms.views import SingleFormView, MultiFormView

from core.auth.views import LoginRequiredMixin


logger = logging.getLogger(__name__)


class SectionDocumentMixin:
    @cached_property
    def application(self):
        application_id = str(self.kwargs["pk"])
        return get_application(self.request, application_id)

    def get_section_document(self):
        documents = {item["document_type"]: item for item in self.application["organisation"]["documents"]}
        good_firearms_details = self.good.get("firearm_details")

        good_firearms_details_act_section = None
        if good_firearms_details:
            good_firearms_details_act_section = good_firearms_details.get("firearms_act_section")

        firearm_section = self.request.POST.get("firearms_act_section") or good_firearms_details_act_section
        if firearm_section == "firearms_act_section1":
            return documents["section-one-certificate"]
        elif firearm_section == "firearms_act_section2":
            return documents["section-two-certificate"]
        elif firearm_section == "firearms_act_section5":
            return documents["section-five-certificate"]


class ApplicationGoodsList(LoginRequiredMixin, TemplateView):

    template_name = "applications/goods/index.html"

    def get_context_data(self, **kwargs):
        application = get_application(self.request, kwargs["pk"])
        goods = get_application_goods(self.request, kwargs["pk"])
        includes_firearms = any(["firearm_details" in good.keys() for good in goods])
        is_exhibition = application["case_type"]["sub_type"]["key"] == constants.EXHIBITION
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


class RegisteredFirearmDealersMixin:
    SESSION_KEY_RFD_CERTIFICATE = "rfd_certificate_details"

    def cache_rfd_certificate_details(self):
        file = self.request.FILES.get("file")
        if not file:
            return
        self.request.session[self.SESSION_KEY_RFD_CERTIFICATE] = {
            "name": getattr(file, "original_name", file.name),
            "s3_key": file.name,
            "size": int(file.size // 1024) if file.size else 0,  # in kilobytes
            "document_on_organisation": {
                "expiry_date": format_date(self.request.POST, "expiry_date_"),
                "reference_code": self.request.POST["reference_code"],
                "document_type": "rfd-certificate",
            },
        }

    def post_success_step(self):
        data = self.request.session.pop(self.SESSION_KEY_RFD_CERTIFICATE, None)
        if data:
            _, status_code = post_additional_document(request=self.request, pk=str(self.kwargs["pk"]), json=data,)
            assert status_code == HTTPStatus.CREATED


class AddGood(LoginRequiredMixin, RegisteredFirearmDealersMixin, MultiFormView):
    STEP_ARE_YOU_RFD = 8
    STEP_RFD_UPLOAD_FORM_TITLE = "Attach your registered firearms dealer certificate"

    @cached_property
    def application(self):
        return get_application(self.request, self.kwargs["pk"])

    @property
    def form_pk(self):
        return int(self.request.POST["form_pk"])

    @property
    def number_of_forms(self):
        # we require the form index of the last form in the group, not the total number
        return len(self.forms.get_forms()) - 1

    def validate_step(self, request, nested_data):
        logger.debug("AddGood validate_step: request=%s nested_data=%s", request, nested_data)
        errors = {}
        current = get_form_by_pk(self.form_pk, self.forms)
        logger.debug("AddGood validate_step: current=%s self.form_pk=%s", current, self.form_pk)
        if self.form_pk == self.STEP_ARE_YOU_RFD:
            if "is_registered_firearm_dealer" not in request.POST:
                errors["is_registered_firearm_dealer"] = ["Select yes if you are a registered firearms dealer"]

        elif current and current.title == self.STEP_RFD_UPLOAD_FORM_TITLE:
            if not self.request.FILES.get("file"):
                errors["file"] = ["Select certificate file to upload"]
            if not self.request.POST.get("reference_code"):
                errors["reference_code"] = ["Enter the certificate number"]
            errors["expiry_date"] = validate_expiry_date(request, "expiry_date_")

        if errors:
            return {"errors": errors}, None
        return validate_good(request, nested_data)

    def init(self, request, **kwargs):
        self.draft_pk = str(kwargs["pk"])
        self.forms = add_good_form_group(request=request, draft_pk=self.draft_pk, application=self.application,)
        self.show_section_upload_form = False

    def on_submission(self, request, **kwargs):
        copied_request = request.POST.copy()
        is_pv_graded = copied_request.get("is_pv_graded", "") == "yes"
        is_software_technology = copied_request.get("item_category") in ["group3_software", "group3_technology"]

        (
            is_firearm,
            is_firearm_ammunition_or_component,
            is_firearms_accessory,
            is_firearms_software_or_tech,
        ) = get_firearms_subcategory(copied_request.get("type"))

        is_rfd = copied_request.get("is_registered_firearm_dealer") == "True" or has_valid_rfd_certificate(
            self.application
        )

        firearm_act_status = copied_request.get("is_covered_by_firearm_act_section_one_two_or_five", "")
        selected_section = copied_request.get("firearms_act_section", "")

        self.covered_by_firearms_act = firearm_act_status == "Yes"
        self.certificate_not_required = firearm_act_status == "No" or firearm_act_status == "Unsure"
        if is_rfd and self.covered_by_firearms_act:
            selected_section = "firearms_act_section5"

        show_serial_numbers_form = True
        if copied_request.get("has_identification_markings") == "False":
            show_serial_numbers_form = False

        if firearm_act_status == "Yes":
            self.show_section_upload_form = is_firearm_certificate_needed(
                application=self.application, selected_section=selected_section
            )

        self.forms = add_good_form_group(
            request=request,
            is_pv_graded=is_pv_graded,
            is_software_technology=is_software_technology,
            is_firearm=is_firearm,
            is_firearm_ammunition_or_component=is_firearm_ammunition_or_component,
            is_firearms_accessory=is_firearms_accessory,
            is_firearms_software_or_tech=is_firearms_software_or_tech,
            draft_pk=self.draft_pk,
            base_form_back_link=reverse("applications:goods", kwargs={"pk": self.kwargs["pk"]}),
            application=self.application,
            show_serial_numbers_form=show_serial_numbers_form,
            is_rfd=is_rfd,
        )

        if self.form_pk == self.number_of_forms:
            if self.show_section_upload_form:
                firearms_data_id = f"post_{request.session['lite_api_user_id']}_{self.draft_pk}"
                session_data = copied_request.dict()
                if "control_list_entries[]" in copied_request:
                    session_data["control_list_entries"] = copied_request.getlist("control_list_entries[]")
                    del session_data["control_list_entries[]"]

                if "firearms_act_section" not in session_data:
                    session_data["firearms_act_section"] = selected_section

                request.session[firearms_data_id] = session_data

    @property
    def action(self):
        current = get_form_by_pk(self.form_pk, self.forms)
        if current and current.title == self.STEP_RFD_UPLOAD_FORM_TITLE:
            self.cache_rfd_certificate_details()
        if self.form_pk == self.number_of_forms:
            if not self.show_section_upload_form:
                self.hide_unused_errors = False
                return post_goods
        return self.validate_step

    def get_success_url(self):
        if self.show_section_upload_form:
            return reverse_lazy("applications:attach-firearms-certificate", kwargs={"pk": self.kwargs["pk"]})
        else:
            good = self.get_validated_data()["good"]
            return reverse_lazy(
                "applications:add_good_summary", kwargs={"pk": self.kwargs["pk"], "good_pk": good["id"]}
            )


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
        elif post_data["firearms_act_section"] == "firearms_act_section5":
            self.selected_section = "Section 5"

        return super().dispatch(request, **kwargs)

    def get(self, request, **kwargs):
        back_link = build_firearm_back_link_create(
            form_url=reverse("applications:new_good", kwargs={"pk": kwargs["pk"]}),
            form_data=request.session.get(self.firearms_data_id, {}),
        )
        form = upload_firearms_act_certificate_form(section=self.selected_section, filename="", back_link=back_link)
        return form_page(request, form)

    def post(self, request, **kwargs):
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

        errors = validate_expiry_date(request, "section_certificate_date_of_expiry")
        if errors:
            form = upload_firearms_act_certificate_form(
                section="section", filename=self.certificate_filename, back_link=back_link,
            )
            return form_page(request, form, data=data, errors={"section_certificate_date_of_expiry": errors})

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
            document_types = {
                "Section 1": "section-one-certificate",
                "Section 2": "section-two-certificate",
                "Section 5": "section-five-certificate",
            }
            doc_data["document_on_organisation"] = {
                "expiry_date": format_date(request.POST, "section_certificate_date_of_expiry"),
                "reference_code": request.POST["section_certificate_number"],
                "document_type": document_types[self.selected_section],
            }
            data, status_code = post_application_document(request, self.draft_pk, self.good_pk, doc_data)
            if status_code != HTTPStatus.CREATED:
                return error_page(request, data["errors"]["file"])
        elif doc_data:
            delete_application_document_data(request, self.draft_pk, self.good_pk, doc_data)

        self.certificate_filename = ""
        del request.session[self.firearms_data_id]
        request.session.pop(file_upload_key, None)
        request.session.modified = True

        return redirect(success_url)


class CheckDocumentAvailability(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.draft_pk = kwargs["pk"]
        self.object_pk = kwargs["good_pk"]
        back_link = reverse("applications:add_good_summary", kwargs={"pk": self.draft_pk, "good_pk": self.object_pk})
        self.data, _ = get_good_document_availability(request, self.object_pk)
        self.form = check_document_available_form(back_link)
        self.action = post_good_document_availability

    def get_data(self):
        value = self.data["good"].get("is_document_available")
        if value is not None:
            value = "yes" if value else "no"
        return {"is_document_available": value}

    def get_success_url(self):
        good = self.get_validated_data()["good"]
        if good["is_document_available"]:
            url = "applications:document_grading"
        else:
            url = "applications:add_good_to_application"
        return (
            reverse_lazy(url, kwargs={"pk": self.draft_pk, "good_pk": self.object_pk})
            + f"?preexisting={self.request.GET.get('preexisting', False)}"
        )


class CheckDocumentGrading(LoginRequiredMixin, SingleFormView):
    def init(self, request, **kwargs):
        self.draft_pk = kwargs["pk"]
        self.object_pk = kwargs["good_pk"]
        back_link = reverse(
            "applications:check_document_availability", kwargs={"pk": self.draft_pk, "good_pk": self.object_pk}
        )
        self.data, _ = get_good_document_sensitivity(request, self.object_pk)
        self.form = document_grading_form(back_link)
        self.action = post_good_document_sensitivity

    def get_data(self):
        value = self.data["good"].get("is_document_sensitive")
        if value is not None:
            value = "yes" if value else "no"
        return {"is_document_sensitive": value}

    def get_success_url(self):
        good = self.get_validated_data()["good"]
        if good["is_document_sensitive"]:
            url = "applications:add_good_to_application"
        else:
            url = "applications:attach_documents"
        return (
            reverse_lazy(url, kwargs={"pk": self.draft_pk, "good_pk": self.object_pk})
            + f"?preexisting={self.request.GET.get('preexisting', False)}"
        )


class AttachDocument(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        good_id = str(kwargs["good_pk"])
        draft_id = str(kwargs["pk"])
        back_link = BackLink(
            "Back", reverse("applications:document_grading", kwargs={"pk": draft_id, "good_pk": good_id})
        )
        form = attach_documents_form(back_link)
        return form_page(request, form, extra_data={"good_id": good_id})

    def post(self, request, **kwargs):
        good_id = str(kwargs["good_pk"])
        draft_id = str(kwargs["pk"])
        back_link = BackLink(
            "Back", reverse("applications:document_grading", kwargs={"pk": draft_id, "good_pk": good_id})
        )

        data, error = add_document_data(request)
        if error:
            form = attach_documents_form(back_link)
            return form_page(request, form, errors={"file": ["Select a document"]})

        data, status_code = post_good_documents(request, good_id, data)
        if status_code != HTTPStatus.CREATED:
            return error_page(request, data["errors"]["file"])

        return redirect(
            reverse_lazy("applications:add_good_to_application", kwargs={"pk": draft_id, "good_pk": good_id})
            + f"?preexisting={self.request.GET.get('preexisting', False)}"
        )


class AddGoodToApplication(LoginRequiredMixin, RegisteredFirearmDealersMixin, SectionDocumentMixin, MultiFormView):
    STEP_RFD_UPLOAD_FORM_TITLE = "Attach your registered firearms dealer certificate"

    @cached_property
    def good(self):
        good, _ = get_good(self.request, self.good_pk)
        return good

    @property
    def form_pk(self):
        return int(self.request.POST["form_pk"])

    @property
    def number_of_forms(self):
        # we require the form index of the last form in the group, not the total number
        return len(self.forms.get_forms()) - 1

    def init(self, request, **kwargs):
        self.object_pk = kwargs["pk"]
        self.good_pk = kwargs["good_pk"]
        self.application = get_application(self.request, self.object_pk)

        self.sub_case_type = self.application["case_type"]["sub_type"]
        is_preexisting = str_to_bool(request.GET.get("preexisting", True))
        show_attach_rfd = str_to_bool(request.POST.get("is_registered_firearm_dealer"))
        is_rfd = show_attach_rfd or has_valid_rfd_certificate(self.application)
        firearm_product_type = self.good["firearm_details"]["type"]["key"]
        (
            is_firearm,
            is_firearm_ammunition_or_component,
            is_firearms_accessory,
            is_firearms_software_or_tech,
        ) = get_firearms_subcategory(firearm_product_type)

        self.forms = good_on_application_form_group(
            request=request,
            is_preexisting=is_preexisting,
            good=self.good,
            sub_case_type=self.sub_case_type,
            draft_pk=self.object_pk,
            application=self.application,
            show_attach_rfd=show_attach_rfd,
            relevant_firearm_act_section=request.POST.get("firearm_act_product_is_coverd_by"),
            is_firearm=is_firearm,
            is_firearm_ammunition_or_component=is_firearm_ammunition_or_component,
            is_firearms_accessory=is_firearms_accessory,
            is_firearms_software_or_tech=is_firearms_software_or_tech,
            back_url=reverse("applications:preexisting_good", kwargs={"pk": self.object_pk}),
            show_serial_numbers_form=True,
            is_rfd=is_rfd,
        )
        self._action = validate_good_on_application
        self.success_url = reverse_lazy(
            "applications:attach-firearms-certificate-existing-good",
            kwargs={"pk": self.object_pk, "good_pk": self.good_pk},
        )

    @property
    def action(self):
        current = get_form_by_pk(self.form_pk, self.forms)
        if current and current.title == self.STEP_RFD_UPLOAD_FORM_TITLE:
            self.cache_rfd_certificate_details()
        return self._action

    def on_submission(self, request, **kwargs):
        is_preexisting = str_to_bool(request.GET.get("preexisting", True))
        copied_request = request.POST.copy()
        show_attach_rfd = str_to_bool(copied_request.get("is_registered_firearm_dealer"))
        relevant_firearm_act_section = copied_request.get("firearm_act_product_is_coverd_by")
        back_url = reverse("applications:preexisting_good", kwargs={"pk": self.good_pk})

        number_of_items = copied_request.get("number_of_items")
        if self.good.get("firearm_details"):
            self.good["firearm_details"]["number_of_items"] = number_of_items

        is_rfd = show_attach_rfd or has_valid_rfd_certificate(self.application)
        selected_section = copied_request.get("firearms_act_section")
        if is_rfd and copied_request.get("is_covered_by_firearm_act_section_one_two_or_five") == "Yes":
            selected_section = "firearms_act_section5"

        show_section_upload_form = False
        if copied_request.get("is_covered_by_firearm_act_section_one_two_or_five") == "Yes":
            show_section_upload_form = is_firearm_certificate_needed(
                application=self.application, selected_section=selected_section
            )

        show_serial_numbers_form = True
        if copied_request.get("has_identification_markings") == "False":
            show_serial_numbers_form = False

        (
            is_firearm,
            is_firearm_ammunition_or_component,
            is_firearms_accessory,
            is_firearms_software_or_tech,
        ) = get_firearms_subcategory(copied_request.get("type"))

        self.forms = good_on_application_form_group(
            request,
            is_preexisting,
            self.good,
            self.sub_case_type,
            self.object_pk,
            self.application,
            show_attach_rfd,
            relevant_firearm_act_section,
            is_firearm=is_firearm,
            is_firearm_ammunition_or_component=is_firearm_ammunition_or_component,
            is_firearms_accessory=is_firearms_accessory,
            is_firearms_software_or_tech=is_firearms_software_or_tech,
            back_url=back_url,
            show_serial_numbers_form=show_serial_numbers_form,
            is_rfd=is_rfd,
        )

        # we require the form index of the last form in the group, not the total number
        if self.form_pk == self.number_of_forms:
            if show_section_upload_form:
                firearms_data_id = f"post_{request.session['lite_api_user_id']}_{self.object_pk}_{self.good_pk}"

                session_data = self.request.POST.copy().dict()
                if "firearms_act_section" not in session_data:
                    session_data["firearms_act_section"] = selected_section

                request.session[firearms_data_id] = session_data
            else:
                self._action = post_good_on_application
                self.success_url = reverse("applications:goods", kwargs={"pk": self.object_pk})

            # if firearm section 5 is selected and the organization already has a valid section 5 then use saved details
            details = self.good["firearm_details"]
            section = None
            if details:
                section = self.request.POST.get("firearms_act_section") or details["firearms_act_section"]

            if not is_firearm_certificate_needed(application=self.application, selected_section=section):
                if section == "firearms_act_section5":
                    document = self.get_section_document()
                    expiry_date = datetime.strptime(document["expiry_date"], "%d %B %Y")
                    self.request.POST = self.request.POST.copy()
                    self.request.POST.update(
                        {
                            "section_certificate_missing": details["section_certificate_missing"],
                            "section_certificate_missing_reason": details["section_certificate_missing_reason"],
                            "section_certificate_number": document["reference_code"],
                            "section_certificate_date_of_expiryday": expiry_date.strftime("%d"),
                            "section_certificate_date_of_expirymonth": expiry_date.strftime("%m"),
                            "section_certificate_date_of_expiryyear": expiry_date.strftime("%Y"),
                            "firearms_certificate_uploaded": bool(details.get("section_certificate_missing_reason")),
                        }
                    )


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
        documents = {
            item["document_type"].replace("-", "_"): item for item in application["organisation"].get("documents", [])
        }

        context = {
            "application_id": application_id,
            "goods": application["goods"],
            "application_status_draft": application["status"]["key"] in ["draft", constants.APPLICANT_EDITING],
            "organisation_documents": documents,
        }
        return render(request, "applications/goods/goods-detail-summary.html", context)


class AddGoodsSummary(LoginRequiredMixin, SectionDocumentMixin, TemplateView):
    template_name = "applications/goods/add-good-detail-summary.html"

    @cached_property
    def good(self):
        good_id = str(self.kwargs["good_pk"])
        return get_good(self.request, good_id, full_detail=True)[0]

    def get_context_data(self, **kwargs):
        application_id = str(self.kwargs["pk"])
        good_id = str(self.kwargs["good_pk"])
        application = get_application(self.request, application_id)
        is_rfd = has_valid_rfd_certificate(application)

        good_application_documents, _ = get_application_documents(self.request, application_id, good_id)

        return super().get_context_data(
            good=self.good,
            application_id=application_id,
            good_id=good_id,
            is_rfd=is_rfd,
            good_application_documents=good_application_documents["documents"],
            section_document=self.get_section_document(),
            **kwargs,
        )


def is_firearm_certificate_needed(application, selected_section):
    firearm_sections = ["firearms_act_section1", "firearms_act_section2"]
    if not has_valid_section_five_certificate(application):
        firearm_sections.append("firearms_act_section5")
    return selected_section in firearm_sections
