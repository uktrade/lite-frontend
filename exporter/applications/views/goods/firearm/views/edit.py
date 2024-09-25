import logging

from deepmerge import always_merger
from http import HTTPStatus

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from core.constants import (
    FirearmsActDocumentType,
    FirearmsActSections,
)
from core.decorators import expect_status

from exporter.applications.services import (
    edit_good_on_application,
    get_application_documents,
)
from exporter.applications.views.goods.common.conditionals import (
    is_pv_graded,
    is_onward_exported,
)
from exporter.applications.views.goods.common.edit import (
    BaseEditProductDocumentAvailability,
    BaseEditProductDescription,
    BaseEditProductDocumentSensitivity,
    BaseEditProductDocumentView,
    BaseProductDocumentUpload,
    BaseProductEditView,
    BaseProductEditWizardView,
)
from exporter.applications.views.goods.common.initial import (
    get_is_onward_exported_initial_data,
    get_onward_altered_processed_initial_data,
    get_onward_incorporated_initial_data,
    get_pv_grading_details_initial_data,
    get_quantity_and_value_initial_data,
)
from exporter.applications.views.goods.common.mixins import (
    ApplicationMixin,
    GoodMixin,
    GoodOnApplicationMixin,
)
from exporter.applications.views.goods.common.payloads import (
    get_cleaned_data,
    get_pv_grading_details_payload,
    ProductEditPVGradingPayloadBuilder,
)
from exporter.applications.views.goods.common.steps import (
    ProductControlListEntryStep,
    ProductNameStep,
)
from exporter.core.forms import CurrentFile
from exporter.core.helpers import (
    convert_api_date_string_to_date,
    get_rfd_certificate,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
    str_to_bool,
)
from core.wizard.conditionals import C
from core.wizard.views import (
    BaseSessionWizardView,
    StepEditView,
)
from exporter.goods.forms.common import (
    ProductOnwardAlteredProcessedForm,
    ProductOnwardExportedForm,
    ProductOnwardIncorporatedForm,
    ProductPVGradingDetailsForm,
    ProductPVGradingForm,
    ProductQuantityAndValueForm,
)
from exporter.goods.forms.firearms import (
    FirearmAttachFirearmCertificateForm,
    FirearmAttachRFDCertificate,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmDeactivationDetailsForm,
    FirearmFirearmAct1968Form,
    FirearmIsDeactivatedForm,
    FirearmMadeBefore1938Form,
    FirearmRegisteredFirearmsDealerForm,
    FirearmReplicaForm,
    FirearmSection5Form,
    FirearmSerialIdentificationMarkingsForm,
    FirearmSerialNumbersForm,
    FirearmYearOfManufactureForm,
)
from exporter.goods.services import edit_firearm

from .actions import (
    GoodOnApplicationFirearmActCertificateAction,
    OrganisationFirearmActCertificateAction,
    IsRfdAction,
    RfdCertificateAction,
)
from .conditionals import (
    has_organisation_firearm_act_document,
    is_deactivated,
    is_product_covered_by_firearm_act_section,
    is_product_made_before_1938,
    is_registered_firearms_dealer,
    is_serial_numbers_available,
)
from .constants import AddGoodFirearmSteps, AddGoodFirearmToApplicationSteps
from .helpers import get_organisation_document_url
from .initial import (
    get_attach_good_on_application_certificate_initial_data,
    get_attach_organisation_certificate_initial_data,
    get_firearm_act_1968_initial_data,
    get_is_covered_by_section_5_initial_data,
    get_is_deactivated_to_standard_initial_data,
    get_serial_numbers_initial_data,
    get_year_of_manufacture_initial_data,
)
from .payloads import (
    FirearmsActPayloadBuilder,
    FirearmEditFirearmsAct1968PayloadBuilder,
    FirearmEditRegisteredFirearmsDealerPayloadBuilder,
    FirearmEditSection5FirearmsAct1968PayloadBuilder,
    FirearmProductOnApplicationSummaryEditIsDeactivatedPayloadBuilder,
    FirearmProductOnApplicationSummaryEditMadeBefore1938PayloadBuilder,
    FirearmProductOnApplicationSummaryEditOnwardExportedPayloadBuilder,
    FirearmProductOnApplicationSummaryEditSerialIdentificationMarkingsPayloadBuilder,
    get_attach_firearm_act_certificate_payload,
    get_deactivation_details_payload,
    get_firearm_details_cleaned_data,
    get_onward_incorporated_payload,
    get_quantity_and_value_payload,
    get_serial_numbers_payload,
)


logger = logging.getLogger(__name__)


class BaseEditView(BaseProductEditView):
    def get_success_url(self):
        return reverse("applications:firearm_product_summary", kwargs=self.kwargs)

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, good_id, payload):
        return edit_firearm(request, good_id, payload)


class BaseGoodEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class BaseFirearmEditView(BaseEditView):
    def get_edit_payload(self, form):
        return get_firearm_details_cleaned_data(form)


class FirearmSummaryMixin:
    def get_success_url(self):
        return reverse("applications:firearm_product_summary", kwargs=self.kwargs)


class EditFirearm:
    @expect_status(
        HTTPStatus.OK,
        "Error editing firearm",
        "Unexpected error editing firearm",
    )
    def edit_firearm(self, request, good_id, form):
        payload = get_cleaned_data(form)
        return edit_firearm(request, good_id, payload)

    def run(self, view, form):
        self.edit_firearm(
            view.request,
            view.good["id"],
            form,
        )


class FirearmEditName(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    FirearmSummaryMixin,
    StepEditView,
):
    actions = (EditFirearm(),)
    step = ProductNameStep()


class FirearmEditCategory(BaseFirearmEditView):
    form_class = FirearmCategoryForm

    def get_initial(self):
        firearm_details = self.good["firearm_details"]
        categories = [category["key"] for category in firearm_details["category"]]
        return {"category": categories}


class FirearmEditCalibre(BaseFirearmEditView):
    form_class = FirearmCalibreForm

    def get_initial(self):
        return {"calibre": self.good["firearm_details"]["calibre"]}


class FirearmEditControlListEntry(
    LoginRequiredMixin,
    ApplicationMixin,
    GoodMixin,
    FirearmSummaryMixin,
    StepEditView,
):
    actions = (EditFirearm(),)
    step = ProductControlListEntryStep()


class FirearmEditReplica(BaseFirearmEditView):
    form_class = FirearmReplicaForm

    def get_initial(self):
        firearm_details = self.good["firearm_details"]
        return {
            "is_replica": firearm_details["is_replica"],
            "replica_description": firearm_details["replica_description"],
        }


class BaseFirearmEditWizardView(BaseProductEditWizardView):
    def get_success_url(self):
        return reverse("applications:firearm_product_summary", kwargs=self.kwargs)

    @expect_status(
        HTTPStatus.OK,
        "Error updating product",
        "Unexpected error updating product",
    )
    def edit_object(self, request, good_pk, payload):
        return edit_firearm(request, good_pk, payload)


class FirearmEditPVGrading(BaseFirearmEditWizardView):
    form_list = [
        (AddGoodFirearmSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodFirearmSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.PV_GRADING_DETAILS: is_pv_graded,
    }

    def get_pv_grading_payload(self, dict):
        return {
            "is_pv_graded": "yes" if dict["is_pv_graded"] else "no",
        }

    def get_form_initial(self, step):
        initial = {}
        if step == AddGoodFirearmSteps.PV_GRADING:
            initial = {"is_pv_graded": str_to_bool(self.good["is_pv_graded"].get("key"))}
        elif step == AddGoodFirearmSteps.PV_GRADING_DETAILS and self.good["pv_grading_details"]:
            initial = get_pv_grading_details_initial_data(self.good)
        return initial

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodFirearmSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def get_payload(self, form_dict):
        return ProductEditPVGradingPayloadBuilder().build(form_dict)


class FirearmEditPVGradingDetails(BaseGoodEditView):
    form_class = ProductPVGradingDetailsForm

    def get_initial(self):
        return get_pv_grading_details_initial_data(self.good)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return {**kwargs, "request": self.request}

    def get_edit_payload(self, form):
        grading_details = get_pv_grading_details_payload(form)
        return {"is_pv_graded": self.good["is_pv_graded"].get("key"), **grading_details}


class FirearmEditProductDocumentView(
    BaseProductDocumentUpload,
    BaseGoodEditView,
):
    pass


class FirearmEditProductDescriptionView(
    BaseEditProductDescription,
    BaseGoodEditView,
):
    pass


class BaseFirearmEditProductDocumentView(
    BaseEditProductDocumentView,
    BaseFirearmEditWizardView,
):
    pass


class FirearmEditProductDocumentSensitivity(
    BaseEditProductDocumentSensitivity,
    BaseFirearmEditProductDocumentView,
):
    pass


class FirearmEditProductDocumentAvailability(
    BaseEditProductDocumentAvailability,
    BaseFirearmEditProductDocumentView,
):
    pass


class FirearmEditRegisteredFirearmsDealer(BaseFirearmEditWizardView):
    form_list = [
        (AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER, FirearmRegisteredFirearmsDealerForm),
        (AddGoodFirearmSteps.FIREARM_ACT_1968, FirearmFirearmAct1968Form),
        (AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE, FirearmAttachRFDCertificate),
        (AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5, FirearmSection5Form),
        (AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY, FirearmAttachSection5LetterOfAuthorityForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.FIREARM_ACT_1968: ~C(is_registered_firearms_dealer),
        AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE: is_registered_firearms_dealer,
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5: C(is_registered_firearms_dealer),
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_5)
        )
        & ~C(has_organisation_firearm_act_document(FirearmsActDocumentType.SECTION_5)),
    }

    def get_attach_rfd_certificate_initial_data(self):
        rfd_certificate = get_rfd_certificate(self.application)
        if not rfd_certificate:
            return {}

        return {
            "expiry_date": convert_api_date_string_to_date(rfd_certificate["expiry_date"]),
            "reference_code": rfd_certificate["reference_code"],
            "file": CurrentFile(
                rfd_certificate["document"]["name"],
                get_organisation_document_url(rfd_certificate),
                rfd_certificate["document"]["safe"],
            ),
        }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER:
            initial["is_registered_firearm_dealer"] = has_valid_organisation_rfd_certificate(self.application)

        if step == AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE:
            initial.update(self.get_attach_rfd_certificate_initial_data())

        if step == AddGoodFirearmSteps.FIREARM_ACT_1968:
            initial.update(get_firearm_act_1968_initial_data(self.good["firearm_details"]))

        if step == AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5:
            initial.update(get_is_covered_by_section_5_initial_data(self.good["firearm_details"]))

        if step == AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY:
            initial.update(
                get_attach_organisation_certificate_initial_data(
                    FirearmsActDocumentType.SECTION_5,
                    self.application,
                    self.good,
                )
            )

        return initial

    def has_skipped_firearms_attach_step(self, form_dict, firearm_details, section_value, attach_step_name):
        firearms_act_section = firearm_details["firearms_act_section"]
        return firearms_act_section == section_value and attach_step_name not in form_dict

    def get_payload(self, form_dict):
        good_payload = FirearmEditRegisteredFirearmsDealerPayloadBuilder().build(form_dict)
        firearms_act_payload = FirearmsActPayloadBuilder(
            self.application,
            good_payload["firearm_details"],
        ).build(form_dict)

        payload = always_merger.merge(good_payload, firearms_act_payload)

        return payload

    def process_forms(self, form_list, form_dict, **kwargs):
        super().process_forms(form_list, form_dict, **kwargs)

        IsRfdAction(
            AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
            self,
        ).run()

        RfdCertificateAction(
            AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE,
            self,
        ).run()

        OrganisationFirearmActCertificateAction(
            self.request,
            FirearmsActDocumentType.SECTION_5,
            self.application,
            self.good,
            self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY),
        ).run()


class FirearmEditSection5FirearmsAct1968(BaseFirearmEditWizardView):
    form_list = [
        (AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5, FirearmSection5Form),
        (AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY, FirearmAttachSection5LetterOfAuthorityForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_5)
        )
        & ~C(has_organisation_firearm_act_document(FirearmsActDocumentType.SECTION_5)),
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5:
            initial.update(get_is_covered_by_section_5_initial_data(self.good["firearm_details"]))

        return initial

    def get_payload(self, form_dict):
        good_payload = payload = FirearmEditSection5FirearmsAct1968PayloadBuilder().build(form_dict)
        firearms_act_payload = FirearmsActPayloadBuilder(
            self.application,
            good_payload["firearm_details"],
        ).build(form_dict)

        payload = always_merger.merge(good_payload, firearms_act_payload)

        return payload

    def process_forms(self, form_list, form_dict, **kwargs):
        super().process_forms(form_list, form_dict, **kwargs)

        OrganisationFirearmActCertificateAction(
            self.request,
            FirearmsActDocumentType.SECTION_5,
            self.application,
            self.good,
            self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY),
        ).run()


class FirearmEditLetterOfAuthority(BaseFirearmEditView):
    form_class = FirearmAttachSection5LetterOfAuthorityForm
    document_type = FirearmsActDocumentType.SECTION_5

    def get_initial(self):
        return get_attach_organisation_certificate_initial_data(
            self.document_type,
            self.application,
            self.good,
        )

    def get_edit_payload(self, form):
        return get_attach_firearm_act_certificate_payload(form)

    def form_valid(self, form):
        response = super().form_valid(form)

        OrganisationFirearmActCertificateAction(
            self.request,
            self.document_type,
            self.application,
            self.good,
            form.cleaned_data,
        ).run()

        return response


class FirearmEditFirearmsAct1968(BaseFirearmEditWizardView):
    form_list = [
        (AddGoodFirearmSteps.FIREARM_ACT_1968, FirearmFirearmAct1968Form),
        (AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY, FirearmAttachSection5LetterOfAuthorityForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_5)
        )
        & ~C(has_organisation_firearm_act_document(FirearmsActDocumentType.SECTION_5)),
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodFirearmSteps.FIREARM_ACT_1968:
            initial.update(get_firearm_act_1968_initial_data(self.good["firearm_details"]))

        if step == AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY:
            initial.update(
                get_attach_organisation_certificate_initial_data(
                    FirearmsActDocumentType.SECTION_5,
                    self.application,
                    self.good,
                )
            )

        return initial

    def get_payload(self, form_dict):
        good_payload = FirearmEditFirearmsAct1968PayloadBuilder().build(form_dict)
        firearms_act_payload = FirearmsActPayloadBuilder(
            self.application,
            good_payload["firearm_details"],
        ).build(form_dict)

        payload = always_merger.merge(good_payload, firearms_act_payload)

        return payload

    def process_forms(self, form_list, form_dict, **kwargs):
        super().process_forms(form_list, form_dict, **kwargs)

        OrganisationFirearmActCertificateAction(
            self.request,
            FirearmsActDocumentType.SECTION_5,
            self.application,
            self.good,
            self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY),
        ).run()


class SummaryTypeMixin:
    SUMMARY_TYPES = [
        "product-on-application-summary",
        "attach-product-on-application-summary",
    ]

    def dispatch(self, request, *args, **kwargs):
        if kwargs["summary_type"] not in self.SUMMARY_TYPES:
            raise Http404("Not a valid summary type")

        return super().dispatch(request, *args, **kwargs)

    def get_summary_url(self):
        summary_url_name = self.kwargs["summary_type"].replace("-", "_")

        return reverse(
            f"applications:{summary_url_name}",
            kwargs={
                "pk": self.application["id"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_success_url(self):
        return self.get_summary_url()

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx["back_link_url"] = self.get_summary_url()

        return ctx


class BaseGoodOnApplicationEditView(
    LoginRequiredMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    FormView,
):
    template_name = "core/form.html"

    @expect_status(
        HTTPStatus.OK,
        "Error updating firearm",
        "Unexpected error updating firearm",
    )
    def edit_firearm_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def perform_actions(self, form):
        self.edit_firearm_good_on_application(
            self.request,
            self.good_on_application["id"],
            self.get_edit_payload(form),
        )

    def form_valid(self, form):
        self.perform_actions(form)
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["form_title"] = self.form_class.Layout.TITLE
        return context

    def get_edit_payload(self, form):
        return get_firearm_details_cleaned_data(form)


class BaseFirearmActCertificateGoodOnApplicationEditView(BaseGoodOnApplicationEditView):
    def get_initial(self):
        application_documents, _ = get_application_documents(
            self.request,
            self.application["id"],
            self.good["id"],
        )
        application_documents = application_documents["documents"]

        good_on_application_documents = {
            document["document_type"]: document
            for document in application_documents
            if document["good_on_application"] == self.good_on_application["id"]
        }

        return get_attach_good_on_application_certificate_initial_data(
            good_on_application_documents[self.document_type],
            self.application,
            self.good,
            self.good_on_application,
        )

    def get_edit_payload(self, form):
        return get_attach_firearm_act_certificate_payload(form)

    def perform_actions(self, form):
        super().perform_actions(form)

        GoodOnApplicationFirearmActCertificateAction(
            self.request,
            self.document_type,
            self.application,
            self.good,
            self.good_on_application,
            form.cleaned_data,
        ).run()


class FirearmProductOnApplicationSummaryEditFirearmCertificate(BaseFirearmActCertificateGoodOnApplicationEditView):
    form_class = FirearmAttachFirearmCertificateForm
    document_type = FirearmsActDocumentType.SECTION_1


class FirearmProductOnApplicationSummaryEditShotgunCertificate(BaseFirearmActCertificateGoodOnApplicationEditView):
    form_class = FirearmAttachFirearmCertificateForm
    document_type = FirearmsActDocumentType.SECTION_2


class BaseProductOnApplicationSummaryEditWizardView(
    LoginRequiredMixin,
    SummaryTypeMixin,
    ApplicationMixin,
    GoodOnApplicationMixin,
    BaseSessionWizardView,
):
    @expect_status(
        HTTPStatus.OK,
        "Error updating firearm",
        "Unexpected error updating firearm",
    )
    def edit_firearm_good_on_application(self, request, good_on_application_id, payload):
        return edit_good_on_application(
            request,
            good_on_application_id,
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        self.edit_firearm_good_on_application(
            self.request,
            self.good_on_application["id"],
            self.get_edit_firearm_good_on_application_payload(form_dict),
        )

        return redirect(self.get_success_url())


class FirearmProductOnApplicationSummaryEditMadeBefore1938(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938, FirearmMadeBefore1938Form),
        (AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE, FirearmYearOfManufactureForm),
    ]
    condition_dict = {
        AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE: is_product_made_before_1938,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        if step == AddGoodFirearmToApplicationSteps.MADE_BEFORE_1938:
            initial["is_made_before_1938"] = self.good_on_application["firearm_details"]["is_made_before_1938"]

        if step == AddGoodFirearmToApplicationSteps.YEAR_OF_MANUFACTURE:
            initial.update(get_year_of_manufacture_initial_data(self.good_on_application["firearm_details"]))

        return initial

    def get_edit_firearm_good_on_application_payload(self, form_dict):
        return FirearmProductOnApplicationSummaryEditMadeBefore1938PayloadBuilder().build(form_dict)


class FirearmProductOnApplicationSummaryEditYearOfManufacture(BaseGoodOnApplicationEditView):
    form_class = FirearmYearOfManufactureForm

    def get_initial(self):
        return get_year_of_manufacture_initial_data(self.good_on_application["firearm_details"])


class FirearmProductOnApplicationSummaryEditOnwardExported(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED, ProductOnwardExportedForm),
        (AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED, ProductOnwardAlteredProcessedForm),
        (AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED, ProductOnwardIncorporatedForm),
    ]
    condition_dict = {
        AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == AddGoodFirearmToApplicationSteps.ONWARD_EXPORTED:
            initial.update(get_is_onward_exported_initial_data(self.good_on_application))

        if step == AddGoodFirearmToApplicationSteps.ONWARD_ALTERED_PROCESSED:
            initial.update(get_onward_altered_processed_initial_data(self.good_on_application))

        if step == AddGoodFirearmToApplicationSteps.ONWARD_INCORPORATED:
            initial.update(get_onward_incorporated_initial_data(self.good_on_application))

        return initial

    def get_edit_firearm_good_on_application_payload(self, form_dict):
        return FirearmProductOnApplicationSummaryEditOnwardExportedPayloadBuilder().build(form_dict)


class FirearmProductOnApplicationSummaryEditOnwardAltered(BaseGoodOnApplicationEditView):
    form_class = ProductOnwardAlteredProcessedForm

    def get_initial(self):
        return get_onward_altered_processed_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        return get_cleaned_data(form)


class FirearmProductOnApplicationSummaryEditOnwardIncorporated(BaseGoodOnApplicationEditView):
    form_class = ProductOnwardIncorporatedForm

    def get_initial(self):
        return get_onward_incorporated_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        return get_onward_incorporated_payload(form)


class FirearmProductOnApplicationSummaryEditIsDeactivated(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodFirearmToApplicationSteps.IS_DEACTIVATED, FirearmIsDeactivatedForm),
        (AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD, FirearmDeactivationDetailsForm),
    ]
    condition_dict = {
        AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD: is_deactivated,
    }

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        firearm_details = self.good_on_application["firearm_details"]

        if step == AddGoodFirearmToApplicationSteps.IS_DEACTIVATED:
            initial["is_deactivated"] = firearm_details["is_deactivated"]

        if step == AddGoodFirearmToApplicationSteps.IS_DEACTIVATED_TO_STANDARD:
            initial.update(get_is_deactivated_to_standard_initial_data(firearm_details))

        return initial

    def get_edit_firearm_good_on_application_payload(self, form_dict):
        return FirearmProductOnApplicationSummaryEditIsDeactivatedPayloadBuilder().build(form_dict)


class FirearmProductOnApplicationSummaryEditIsDeactivatedToStandard(BaseGoodOnApplicationEditView):
    form_class = FirearmDeactivationDetailsForm

    def get_initial(self):
        return get_is_deactivated_to_standard_initial_data(self.good_on_application["firearm_details"])

    def get_edit_payload(self, form):
        return get_deactivation_details_payload(form)


class FirearmProductOnApplicationSummaryEditQuantityValue(BaseGoodOnApplicationEditView):
    form_class = ProductQuantityAndValueForm

    def get_initial(self):
        return get_quantity_and_value_initial_data(self.good_on_application)

    def get_edit_payload(self, form):
        return get_quantity_and_value_payload(form)


class FirearmProductOnApplicationSummaryEditSerialIdentificationMarkings(BaseProductOnApplicationSummaryEditWizardView):
    form_list = [
        (AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING, FirearmSerialIdentificationMarkingsForm),
        (AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS, FirearmSerialNumbersForm),
    ]
    condition_dict = {
        AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS: is_serial_numbers_available,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        if step == AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS:
            kwargs["number_of_items"] = int(self.good_on_application["quantity"])
        return kwargs

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)

        firearm_details = self.good_on_application["firearm_details"]

        if step == AddGoodFirearmToApplicationSteps.SERIAL_IDENTIFICATION_MARKING:
            initial.update(
                {
                    "serial_numbers_available": firearm_details["serial_numbers_available"],
                    "no_identification_markings_details": firearm_details["no_identification_markings_details"],
                }
            )

        if step == AddGoodFirearmToApplicationSteps.SERIAL_NUMBERS:
            initial.update(get_serial_numbers_initial_data(firearm_details))

        return initial

    def get_edit_firearm_good_on_application_payload(self, form_dict):
        return FirearmProductOnApplicationSummaryEditSerialIdentificationMarkingsPayloadBuilder().build(form_dict)


class FirearmProductOnApplicationSummaryEditSerialNumbers(BaseGoodOnApplicationEditView):
    form_class = FirearmSerialNumbersForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs["number_of_items"] = int(self.good_on_application["quantity"])

        return kwargs

    def get_initial(self):
        return get_serial_numbers_initial_data(self.good_on_application["firearm_details"])

    def get_edit_payload(self, form):
        return get_serial_numbers_payload(form)
