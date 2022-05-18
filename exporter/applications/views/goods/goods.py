import logging
from datetime import datetime
from http import HTTPStatus

from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import TemplateView
from formtools.wizard.storage.session import SessionStorage

from core.auth.views import LoginRequiredMixin
from core.helpers import convert_dict_to_query_params
from exporter.applications.helpers.check_your_answers import get_total_goods_value
from exporter.applications.helpers.date_fields import format_date
from exporter.applications.services import (
    add_document_data,
    delete_application_document_data,
    delete_application_preexisting_good,
    download_document_from_s3,
    get_application,
    get_application_document,
    get_application_documents,
    get_application_goods,
    get_applications_require_serial_numbers,
    post_additional_document,
    post_application_document,
    post_good_on_application,
)
from exporter.core import constants
from exporter.core.constants import AddGoodFormSteps
from exporter.core.helpers import (
    has_valid_rfd_certificate,
    is_category_firearms,
    is_draft,
    is_preexisting,
    is_product_type,
    is_pv_graded,
    show_attach_rfd_form,
    show_rfd_form,
    show_serial_numbers_form,
    str_to_bool,
)
from exporter.core.validators import validate_expiry_date
from exporter.core.wizard.conditionals import C, Flag
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms import (
    AddGoodsQuestionsForm,
    AttachFirearmsDealerCertificateForm,
    ComponentOfAFirearmAmmunitionUnitQuantityValueForm,
    ComponentOfAFirearmUnitQuantityValueForm,
    FirearmsActConfirmationForm,
    FirearmsCalibreDetailsForm,
    FirearmsCaptureSerialNumbersForm,
    FirearmsNumberOfItemsForm,
    FirearmsReplicaForm,
    FirearmsUnitQuantityValueForm,
    FirearmsYearOfManufactureDetailsForm,
    GroupTwoProductTypeForm,
    IdentificationMarkingsForm,
    ProductCategoryForm,
    ProductComponentForm,
    ProductMilitaryUseForm,
    ProductUsesInformationSecurityForm,
    PvDetailsForm,
    RegisteredFirearmsDealerForm,
    SoftwareTechnologyDetailsForm,
    UnitQuantityValueForm,
    attach_documents_form,
    build_firearm_back_link_create,
    check_document_available_form,
    document_grading_form,
    has_valid_section_five_certificate,
    upload_firearms_act_certificate_form,
)
from exporter.goods.services import (
    get_good,
    get_good_document_availability,
    get_good_document_sensitivity,
    get_goods,
    post_good_document_availability,
    post_good_document_sensitivity,
    post_good_documents,
    post_goods,
)
from lite_forms.components import BackLink, FiltersBar, TextInput
from lite_forms.generators import error_page, form_page
from lite_forms.views import SingleFormView

log = logging.getLogger(__name__)


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
        if firearm_section == constants.FirearmsActSections.SECTION_1:
            return documents[constants.FirearmsActDocumentType.SECTION_1]
        elif firearm_section == constants.FirearmsActSections.SECTION_2:
            return documents[constants.FirearmsActDocumentType.SECTION_2]
        elif firearm_section == constants.FirearmsActSections.SECTION_5:
            return documents[constants.FirearmsActDocumentType.SECTION_5]


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
            "feature_flag_product_2_0": settings.FEATURE_FLAG_PRODUCT_2_0,
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
                "document_type": constants.DocumentType.RFD_CERTIFICATE,
            },
        }

    def post_success_step(self):
        data = self.request.session.pop(self.SESSION_KEY_RFD_CERTIFICATE, None)
        if data:
            _, status_code = post_additional_document(
                request=self.request,
                pk=str(self.kwargs["pk"]),
                json=data,
            )
            assert status_code == HTTPStatus.CREATED


class SkipResetSessionStorage(SessionStorage):
    """This gives clients the ability to skip the reset (deletion) of
    data that has been collected by the wizard.
    """

    def skip_reset(self):
        """Tell the storage to skip the next reset() operation."""
        self.request.session["skip_reset"] = True

    def reset(self):
        """Resets the storage and deletes any data unless unless
        skip_reset() has been called beforehand.
        """
        if not self.request.session.pop("skip_reset", None):
            super().reset()


class AddGood(LoginRequiredMixin, BaseSessionWizardView):
    """This view manages the sequence of forms that are used add a new product
    to an existing application.
    """

    storage_name = "exporter.applications.views.goods.SkipResetSessionStorage"

    form_list = [
        (AddGoodFormSteps.PRODUCT_CATEGORY, ProductCategoryForm),
        (AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE, GroupTwoProductTypeForm),
        (AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS, FirearmsNumberOfItemsForm),
        (AddGoodFormSteps.IDENTIFICATION_MARKINGS, IdentificationMarkingsForm),
        (AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS, FirearmsCaptureSerialNumbersForm),
        (AddGoodFormSteps.PRODUCT_MILITARY_USE, ProductMilitaryUseForm),
        (AddGoodFormSteps.PRODUCT_USES_INFORMATION_SECURITY, ProductUsesInformationSecurityForm),
        (AddGoodFormSteps.ADD_GOODS_QUESTIONS, AddGoodsQuestionsForm),
        (AddGoodFormSteps.PV_DETAILS, PvDetailsForm),
        (AddGoodFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS, FirearmsYearOfManufactureDetailsForm),
        (AddGoodFormSteps.FIREARMS_REPLICA, FirearmsReplicaForm),
        (AddGoodFormSteps.FIREARMS_CALIBRE_DETAILS, FirearmsCalibreDetailsForm),
        (AddGoodFormSteps.REGISTERED_FIREARMS_DEALER, RegisteredFirearmsDealerForm),
        (AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE, AttachFirearmsDealerCertificateForm),
        (AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION, FirearmsActConfirmationForm),
        (AddGoodFormSteps.SOFTWARE_TECHNOLOGY_DETAILS, SoftwareTechnologyDetailsForm),
        (AddGoodFormSteps.PRODUCT_MILITARY_USE_ACC_TECH, ProductMilitaryUseForm),
        (AddGoodFormSteps.PRODUCT_COMPONENT, ProductComponentForm),
        (AddGoodFormSteps.PRODUCT_USES_INFORMATION_SECURITY_ACC_TECH, ProductUsesInformationSecurityForm),
    ]

    condition_dict = {
        AddGoodFormSteps.PRODUCT_CATEGORY: ~Flag(settings, "FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS"),
        AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE: is_category_firearms,
        AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS: C(is_draft) & C(is_product_type("ammunition_or_component")),
        AddGoodFormSteps.IDENTIFICATION_MARKINGS: C(is_draft) & C(is_product_type("ammunition_or_component")),
        AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS: (
            C(is_draft)
            & C(is_product_type("ammunition_or_component"))
            & C(show_serial_numbers_form(AddGoodFormSteps.IDENTIFICATION_MARKINGS))
        ),
        AddGoodFormSteps.PRODUCT_MILITARY_USE: ~C(is_category_firearms),
        AddGoodFormSteps.PRODUCT_USES_INFORMATION_SECURITY: ~C(is_category_firearms),
        AddGoodFormSteps.PV_DETAILS: is_pv_graded,
        AddGoodFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS: C(is_draft) & C(is_product_type("firearm")),
        AddGoodFormSteps.FIREARMS_REPLICA: is_product_type("firearm"),
        AddGoodFormSteps.FIREARMS_CALIBRE_DETAILS: is_product_type("ammunition_or_component"),
        AddGoodFormSteps.REGISTERED_FIREARMS_DEALER: show_rfd_form,
        AddGoodFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE: show_attach_rfd_form,
        AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION: C(is_draft) & C(is_product_type("ammunition_or_component")),
        AddGoodFormSteps.SOFTWARE_TECHNOLOGY_DETAILS: is_product_type("firearms_software_or_tech"),
        AddGoodFormSteps.PRODUCT_MILITARY_USE_ACC_TECH: (
            C(is_product_type("firearms_accessory")) | C(is_product_type("firearms_software_or_tech"))
        ),
        AddGoodFormSteps.PRODUCT_COMPONENT: is_product_type("firearms_accessory"),
        AddGoodFormSteps.PRODUCT_USES_INFORMATION_SECURITY_ACC_TECH: (
            C(is_product_type("firearms_accessory")) | C(is_product_type("firearms_software_or_tech"))
        ),
    }

    @cached_property
    def application(self):
        return get_application(self.request, self.kwargs["pk"])

    def get_product_type(self):
        group_two_product_type_cleaned_data = self.get_cleaned_data_for_step(AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE)

        if group_two_product_type_cleaned_data:
            return group_two_product_type_cleaned_data["type"]

        return None

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context["title"] = form.title
        # The back_link_url is used for the first form in the sequence. For subsequent forms,
        # the wizard automatically generates the back link to the previous form.
        context["back_link_url"] = reverse("applications:goods", kwargs={"pk": self.kwargs["pk"]})
        return context

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS:
            kwargs["number_of_items"] = self.get_cleaned_data_for_step(AddGoodFormSteps.FIREARMS_NUMBER_OF_ITEMS).get(
                "number_of_items", 0
            )

        if step == AddGoodFormSteps.ADD_GOODS_QUESTIONS:
            kwargs["request"] = self.request
            kwargs["application_pk"] = str(self.kwargs["pk"])

        if step == AddGoodFormSteps.PV_DETAILS:
            kwargs["request"] = self.request

        if step == AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION:
            kwargs["is_rfd"] = str_to_bool(
                self.get_cleaned_data_for_step(AddGoodFormSteps.REGISTERED_FIREARMS_DEALER).get(
                    "is_registered_firearm_dealer"
                )
                or has_valid_rfd_certificate(self.application)
            )

        if step == AddGoodFormSteps.SOFTWARE_TECHNOLOGY_DETAILS:
            kwargs["product_type"] = self.get_cleaned_data_for_step(AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE).get("type")

        return kwargs

    def render_next_step(self, form, **kwargs):
        if settings.FEATURE_FLAG_PRODUCT_2_0 and self.steps.current == AddGoodFormSteps.GROUP_TWO_PRODUCT_TYPE:
            if form.cleaned_data["type"] == "firearms":
                return redirect("applications:new_good_firearm", pk=self.kwargs["pk"])
        return super().render_next_step(form, **kwargs)

    def done(self, form_list, **kwargs):
        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        cert_file = all_data.pop("file", None)

        if not all_data.get("firearms_act_section"):
            is_rfd = str_to_bool(all_data.get("is_registered_firearm_dealer")) or has_valid_rfd_certificate(
                self.application
            )

            if is_rfd and str_to_bool(all_data.get("is_covered_by_firearm_act_section_one_two_or_five")):
                all_data["firearms_act_section"] = "firearms_act_section5"

        # post_goods() modifies the data dict, so pass a copy as we need it unaltered later on
        api_resp_data, status_code = post_goods(self.request, dict(all_data))

        if status_code != HTTPStatus.CREATED:
            log.error(
                "Error creating good - response was: %s - %s",
                status_code,
                api_resp_data,
                exc_info=True,
            )
            return error_page(self.request, "Unexpected error adding good")

        if cert_file:
            rfd_cert = {
                "name": getattr(cert_file, "original_name", cert_file.name),
                "s3_key": cert_file.name,
                "size": int(cert_file.size // 1024) if cert_file.size else 0,  # in kilobytes
                "document_on_organisation": {
                    "expiry_date": format_date(all_data, "expiry_date_"),
                    "reference_code": all_data["reference_code"],
                    "document_type": constants.DocumentType.RFD_CERTIFICATE,
                },
            }

            _, status_code = post_additional_document(
                request=self.request,
                pk=str(self.kwargs["pk"]),
                json=rfd_cert,
            )
            assert status_code == HTTPStatus.CREATED

        if str_to_bool(all_data.get("is_covered_by_firearm_act_section_one_two_or_five")):
            if is_firearm_certificate_needed(
                application=self.application, selected_section=all_data["firearms_act_section"]
            ):
                pk = str(self.kwargs["pk"])
                firearms_data_id = f"post_{self.request.session['lite_api_user_id']}_{pk}"

                all_data["form_pk"] = 0  # Temporary until attach-firearms-certificate is converted to Django form
                all_data["wizard_goto_step"] = AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION
                self.request.session[firearms_data_id] = all_data

                # Don't reset the data in case a user re-enters this wizard from the 'Back' link.
                # Note that data does get reset when a user re-enters the wizard from fresh.
                self.storage.skip_reset()

                return redirect(reverse("applications:attach-firearms-certificate", kwargs={"pk": self.kwargs["pk"]}))

        return redirect(
            reverse(
                "applications:add_good_summary",
                kwargs={"pk": self.kwargs["pk"], "good_pk": api_resp_data["good"]["id"]},
            )
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

        if post_data["firearms_act_section"] == constants.FirearmsActSections.SECTION_1:
            self.selected_section = "Section 1"
        elif post_data["firearms_act_section"] == constants.FirearmsActSections.SECTION_2:
            self.selected_section = "Section 2"
        elif post_data["firearms_act_section"] == constants.FirearmsActSections.SECTION_5:
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
            form_url=reverse("applications:new_good", kwargs={"pk": kwargs["pk"]}),
            form_data=old_post,
        )

        if not request.FILES.get("file"):
            form = upload_firearms_act_certificate_form(
                section="section",
                filename=self.certificate_filename,
                back_link=back_link,
            )
            return form_page(request, form, data=data, errors={"file": ["Select certificate file to upload"]})

        errors = validate_expiry_date(request, "section_certificate_date_of_expiry")
        if errors:
            form = upload_firearms_act_certificate_form(
                section="section",
                filename=self.certificate_filename,
                back_link=back_link,
            )
            return form_page(request, form, data=data, errors={"section_certificate_date_of_expiry": errors})

        if self.good_pk:
            response, status_code = post_good_on_application(request, self.draft_pk, data)
            if status_code != HTTPStatus.CREATED:
                if doc_error:
                    response["errors"]["file"] = ["Select certificate file to upload"]
                form = upload_firearms_act_certificate_form(
                    section="section",
                    filename=self.certificate_filename,
                    back_link=back_link,
                )
                return form_page(request, form, data=data, errors=response["errors"])

            success_url = reverse_lazy("applications:goods", kwargs={"pk": self.draft_pk})

        else:
            response, status_code = post_goods(request, data)
            if status_code != HTTPStatus.CREATED:
                if doc_error:
                    response["errors"]["file"] = ["Select certificate file to upload"]
                form = upload_firearms_act_certificate_form(
                    section="section",
                    filename=self.certificate_filename,
                    back_link=back_link,
                )
                return form_page(request, form, data=data, errors=response["errors"])

            self.good_pk = response["good"]["id"]
            success_url = reverse(
                "applications:add_good_summary", kwargs={"pk": self.draft_pk, "good_pk": self.good_pk}
            )

        if certificate_available and new_file_selected:
            document_types = {
                "Section 1": constants.FirearmsActDocumentType.SECTION_1,
                "Section 2": constants.FirearmsActDocumentType.SECTION_2,
                "Section 5": constants.FirearmsActDocumentType.SECTION_5,
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


class AddGoodToApplicationFormSteps:
    FIREARMS_NUMBER_OF_ITEMS = "FIREARMS_NUMBER_OF_ITEMS"
    IDENTIFICATION_MARKINGS = "IDENTIFICATION_MARKINGS"
    FIREARMS_CAPTURE_SERIAL_NUMBERS = "FIREARMS_CAPTURE_SERIAL_NUMBERS"
    FIREARMS_YEAR_OF_MANUFACTURE_DETAILS = "FIREARMS_YEAR_OF_MANUFACTURE_DETAILS"
    FIREARM_UNIT_QUANTITY_VALUE = "FIREARM_UNIT_QUANTITY_VALUE"
    COMPONENT_OF_A_FIREARM_UNIT_QUANTITY_VALUE = "COMPONENT_OF_A_FIREARM_UNIT_QUANTITY_VALUE"
    COMPONENT_OF_A_FIREARM_AMMUNITION_UNIT_QUANTITY_VALUE = "COMPONENT_OF_A_FIREARM_AMMUNITION_UNIT_QUANTITY_VALUE"
    UNIT_QUANTITY_VALUE = "UNIT_QUANTITY_VALUE"
    REGISTERED_FIREARMS_DEALER = "REGISTERED_FIREARMS_DEALER"
    ATTACH_FIREARM_DEALER_CERTIFICATE = "ATTACH_FIREARM_DEALER_CERTIFICATE"
    FIREARMS_ACT_CONFIRMATION = "FIREARMS_ACT_CONFIRMATION"


def show_rfd_question(wizard):
    is_firearm_ammunition_or_component = is_product_type("ammunition_or_component")(wizard)

    return is_firearm_ammunition_or_component and not has_valid_rfd_certificate(wizard.application)


def show_attach_rfd_question(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER)

    if not cleaned_data:
        return False

    return str_to_bool(cleaned_data.get("is_registered_firearm_dealer"))


def is_product_category(category):
    def _is_product_category(wizard):
        good = wizard.good
        return good["item_category"]["key"] == category

    return _is_product_category


def is_firearm_type_in(firearm_types):
    def _is_firearm_type_in(wizard):
        good = wizard.good
        firearm_type = good["firearm_details"]["type"]["key"]
        return firearm_type in firearm_types

    return _is_firearm_type_in


def is_firearm_type_not_in(firearm_types):
    def _is_firearm_type_not_in(wizard):
        return not is_firearm_type_in(firearm_types)(wizard)

    return _is_firearm_type_not_in


class AddGoodToApplication(SectionDocumentMixin, LoginRequiredMixin, BaseSessionWizardView):
    storage_name = "exporter.applications.views.goods.SkipResetSessionStorage"

    form_list = [
        (AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS, FirearmsNumberOfItemsForm),
        (AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS, IdentificationMarkingsForm),
        (AddGoodToApplicationFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS, FirearmsCaptureSerialNumbersForm),
        (AddGoodToApplicationFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS, FirearmsYearOfManufactureDetailsForm),
        (AddGoodToApplicationFormSteps.FIREARM_UNIT_QUANTITY_VALUE, FirearmsUnitQuantityValueForm),
        (
            AddGoodToApplicationFormSteps.COMPONENT_OF_A_FIREARM_UNIT_QUANTITY_VALUE,
            ComponentOfAFirearmUnitQuantityValueForm,
        ),
        (
            AddGoodToApplicationFormSteps.COMPONENT_OF_A_FIREARM_AMMUNITION_UNIT_QUANTITY_VALUE,
            ComponentOfAFirearmAmmunitionUnitQuantityValueForm,
        ),
        (AddGoodToApplicationFormSteps.UNIT_QUANTITY_VALUE, UnitQuantityValueForm),
        (AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER, RegisteredFirearmsDealerForm),
        (AddGoodToApplicationFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE, AttachFirearmsDealerCertificateForm),
        (AddGoodToApplicationFormSteps.FIREARMS_ACT_CONFIRMATION, FirearmsActConfirmationForm),
    ]

    condition_dict = {
        AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS: (
            C(is_preexisting(True)) & C(is_product_type("ammunition_or_component"))
        ),
        AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS: (
            C(is_preexisting(True)) & C(is_product_type("ammunition_or_component"))
        ),
        AddGoodToApplicationFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS: (
            C(is_preexisting(True))
            & C(is_product_type("ammunition_or_component"))
            & C(show_serial_numbers_form(AddGoodToApplicationFormSteps.IDENTIFICATION_MARKINGS))
        ),
        AddGoodToApplicationFormSteps.FIREARMS_YEAR_OF_MANUFACTURE_DETAILS: (
            C(is_preexisting(True)) & C(is_product_type("firearm"))
        ),
        AddGoodToApplicationFormSteps.FIREARM_UNIT_QUANTITY_VALUE: (
            C(is_product_category(constants.PRODUCT_CATEGORY_FIREARM))
            & C(is_firearm_type_in(constants.FIREARM_AMMUNITION_COMPONENT_TYPES))
            & C(is_firearm_type_not_in([constants.FIREARM_COMPONENT, "components_for_ammunition"]))
        ),
        AddGoodToApplicationFormSteps.COMPONENT_OF_A_FIREARM_UNIT_QUANTITY_VALUE: (
            C(is_product_category(constants.PRODUCT_CATEGORY_FIREARM))
            & C(is_firearm_type_in([constants.FIREARM_COMPONENT]))
        ),
        AddGoodToApplicationFormSteps.COMPONENT_OF_A_FIREARM_AMMUNITION_UNIT_QUANTITY_VALUE: (
            C(is_product_category(constants.PRODUCT_CATEGORY_FIREARM))
            & C(is_firearm_type_in(["components_for_ammunition"]))
        ),
        AddGoodToApplicationFormSteps.UNIT_QUANTITY_VALUE: (
            C(is_product_category(constants.PRODUCT_CATEGORY_FIREARM))
            & C(is_firearm_type_not_in(constants.FIREARM_AMMUNITION_COMPONENT_TYPES))
        ),
        AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER: C(is_preexisting(True)) & C(show_rfd_question),
        AddGoodToApplicationFormSteps.ATTACH_FIREARM_DEALER_CERTIFICATE: (
            C(is_preexisting(True)) & C(show_attach_rfd_question)
        ),
        AddGoodToApplicationFormSteps.FIREARMS_ACT_CONFIRMATION: (
            C(is_preexisting(True)) & C(is_product_type("ammunition_or_component"))
        ),
    }

    @cached_property
    def application(self):
        return get_application(self.request, self.kwargs["pk"])

    @cached_property
    def good(self):
        good, _ = get_good(self.request, self.kwargs["good_pk"])
        return good

    def get_product_type(self):
        return self.good["firearm_details"]["type"]["key"]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context["title"] = form.title
        # The back_link_url is used for the first form in the sequence. For subsequent forms,
        # the wizard automatically generates the back link to the previous form.
        context["back_link_url"] = reverse_lazy("applications:preexisting_good", kwargs={"pk": self.kwargs["pk"]})
        return context

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodToApplicationFormSteps.FIREARMS_CAPTURE_SERIAL_NUMBERS:
            kwargs["number_of_items"] = self.get_cleaned_data_for_step(
                AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS
            ).get("number_of_items", 0)

        if step in (
            AddGoodToApplicationFormSteps.FIREARM_UNIT_QUANTITY_VALUE,
            AddGoodToApplicationFormSteps.COMPONENT_OF_A_FIREARM_UNIT_QUANTITY_VALUE,
            AddGoodToApplicationFormSteps.COMPONENT_OF_A_FIREARM_AMMUNITION_UNIT_QUANTITY_VALUE,
            AddGoodToApplicationFormSteps.UNIT_QUANTITY_VALUE,
        ):
            kwargs["good"] = self.good

            # The number of items can be derived from two different places.
            # Either because it has been set explicitly by the user as part of
            # a previous step within this wizard flow or from a previously saved
            # good.
            # We always try to default to default to whatever the user input on
            # this wizard, if not we defer back to the saved good and then
            # eventually if neither return we return a sensible default.
            kwargs["number_of_items"] = self.get_cleaned_data_for_step(
                AddGoodToApplicationFormSteps.FIREARMS_NUMBER_OF_ITEMS
            ).get(
                "number_of_items",
                self.good["firearm_details"].get("number_of_items", 0),
            )

        if step == AddGoodToApplicationFormSteps.UNIT_QUANTITY_VALUE:
            kwargs["request"] = self.request

        if step == AddGoodToApplicationFormSteps.FIREARMS_ACT_CONFIRMATION:
            try:
                is_registered_firearm_dealer = self.get_cleaned_data_for_step(
                    AddGoodToApplicationFormSteps.REGISTERED_FIREARMS_DEALER
                ).get("is_registered_firearm_dealer")
            except AttributeError:
                is_registered_firearm_dealer = False
            kwargs["is_rfd"] = str_to_bool(is_registered_firearm_dealer or has_valid_rfd_certificate(self.application))

        return kwargs

    def get_good_on_application_data(self, form_list):
        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}

        all_data["pk"] = str(self.kwargs["pk"])

        good = self.good
        all_data["good_id"] = str(good["id"])

        firearm_type = None
        if good.get("firearm_details"):
            if not all_data.get("number_of_items"):
                all_data["number_of_items"] = good["firearm_details"]["number_of_items"]
            firearm_type = good["firearm_details"]["type"]["key"]
        all_data["type"] = firearm_type

        return all_data

    def should_show_section_upload_form(self, all_data, selected_section):
        show_section_upload_form = False
        if all_data.get("is_covered_by_firearm_act_section_one_two_or_five") == "Yes":
            show_section_upload_form = is_firearm_certificate_needed(
                application=self.application, selected_section=selected_section
            )
        return show_section_upload_form

    def get_selected_section(self, all_data):
        show_attach_rfd = str_to_bool(all_data.get("is_registered_firearm_dealer"))
        is_rfd = show_attach_rfd or has_valid_rfd_certificate(self.application)
        selected_section = all_data.get("firearms_act_section")
        if is_rfd and all_data.get("is_covered_by_firearm_act_section_one_two_or_five") == "Yes":
            selected_section = "firearms_act_section5"

        return selected_section

    def get_section_document(self, all_data):
        documents = {item["document_type"]: item for item in self.application["organisation"]["documents"]}
        good_firearms_details = self.good.get("firearm_details")

        good_firearms_details_act_section = None
        if good_firearms_details:
            good_firearms_details_act_section = good_firearms_details.get("firearms_act_section")

        firearm_section = all_data.get("firearms_act_section") or good_firearms_details_act_section
        if firearm_section == constants.FirearmsActSections.SECTION_1:
            return documents[constants.FirearmsActDocumentType.SECTION_1]
        elif firearm_section == constants.FirearmsActSections.SECTION_2:
            return documents[constants.FirearmsActDocumentType.SECTION_2]
        elif firearm_section == constants.FirearmsActSections.SECTION_5:
            return documents[constants.FirearmsActDocumentType.SECTION_5]

    def done(self, form_list, **kwargs):
        all_data = self.get_good_on_application_data(form_list)
        cert_file = all_data.pop("file", None)

        if cert_file:
            rfd_cert = {
                "name": getattr(cert_file, "original_name", cert_file.name),
                "s3_key": cert_file.name,
                "size": int(cert_file.size // 1024) if cert_file.size else 0,  # in kilobytes
                "document_on_organisation": {
                    "expiry_date": format_date(all_data, "expiry_date_"),
                    "reference_code": all_data["reference_code"],
                    "document_type": constants.DocumentType.RFD_CERTIFICATE,
                },
            }

            _, status_code = post_additional_document(request=self.request, pk=str(self.kwargs["pk"]), json=rfd_cert)
            assert status_code == HTTPStatus.CREATED

        selected_section = self.get_selected_section(all_data)
        if self.should_show_section_upload_form(all_data, selected_section):
            firearms_data_id = f"post_{self.request.session['lite_api_user_id']}_{self.kwargs['pk']}_{self.good['id']}"

            if "firearms_act_section" not in all_data or not all_data.get("firearms_act_section"):
                all_data["firearms_act_section"] = selected_section

            all_data["form_pk"] = 1
            all_data["wizard_goto_step"] = AddGoodFormSteps.FIREARMS_ACT_CONFIRMATION
            self.request.session[firearms_data_id] = all_data

            # Don't reset the data in case a user re-enters this wizard from the 'Back' link.
            # Note that data does get reset when a user re-enters the wizard from fresh.
            self.storage.skip_reset()

            return redirect(
                reverse(
                    "applications:attach-firearms-certificate-existing-good",
                    kwargs={
                        "pk": self.kwargs["pk"],
                        "good_pk": self.good["id"],
                    },
                ),
            )

        # if firearm section 5 is selected and the organization already has a valid section 5 then use saved details
        details = self.good["firearm_details"]
        section = None
        if details:
            section = all_data.get("firearms_act_section") or details["firearms_act_section"]

        if not is_firearm_certificate_needed(application=self.application, selected_section=section):
            if section == "firearms_act_section5":
                document = self.get_section_document(all_data)
                expiry_date = datetime.strptime(document["expiry_date"], "%d %B %Y")
                all_data.update(
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

        api_resp_data, status_code = post_good_on_application(self.request, self.application["id"], all_data)

        if status_code != HTTPStatus.CREATED:
            log.error(
                "Error adding good to application - response was: %s - %s",
                status_code,
                api_resp_data,
                exc_info=True,
            )
            return error_page(self.request, "Unexpected error adding good")

        return redirect(
            reverse(
                "applications:goods",
                kwargs={
                    "pk": self.kwargs["pk"],
                },
            ),
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
    template_name = "applications/goods/goods-detail-summary.html"

    def get_context_data(self, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(self.request, application_id)
        documents = {
            item["document_type"].replace("-", "_"): item for item in application["organisation"].get("documents", [])
        }

        return {
            "application_id": application_id,
            "goods": application["goods"],
            "is_user_rfd": has_valid_rfd_certificate(application),
            "application_status_draft": application["status"]["key"] in ["draft", constants.APPLICANT_EDITING],
            "organisation_documents": documents,
            "feature_flag_product_2_0": settings.FEATURE_FLAG_PRODUCT_2_0,
        }


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
    firearm_sections = [constants.FirearmsActSections.SECTION_1, constants.FirearmsActSections.SECTION_2]
    if not has_valid_section_five_certificate(application):
        firearm_sections.append("firearms_act_section5")
    return selected_section in firearm_sections


class AddSerialNumbersList(LoginRequiredMixin, TemplateView):
    template_name = "applications/goods/add-serial-numbers-list.html"

    @cached_property
    def applications(self):
        params = {"page": int(self.request.GET.get("page", 1))}
        response = get_applications_require_serial_numbers(self.request, **params)
        return response["results"]

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx["applications"] = self.applications

        return ctx
