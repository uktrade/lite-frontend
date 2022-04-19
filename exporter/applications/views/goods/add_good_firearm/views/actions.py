from http import HTTPStatus

from exporter.applications.services import (
    post_additional_document,
    post_application_document,
)
from exporter.core.constants import DocumentType
from exporter.core.forms import CurrentFile
from exporter.core.helpers import (
    get_document_data,
    get_firearm_act_document,
    get_rfd_certificate,
    has_valid_rfd_certificate,
)
from exporter.organisation.services import update_document_on_organisation

from .decorators import expect_status


class CreateOrUpdateFirearmActCertificateAction:
    def __init__(self, step_name, document_type, wizard):
        self.step_name = step_name
        self.document_type = document_type
        self.wizard = wizard
        self.request = wizard.request
        self.application = wizard.application
        self.good = wizard.good

    def has_firearm_act_certificate(self):
        attach_firearm_certificate = self.wizard.get_cleaned_data_for_step(self.step_name)
        return bool(attach_firearm_certificate.get("file"))

    def is_new_firearm_act_certificate(self):
        attach_firearm_certificate = self.wizard.get_cleaned_data_for_step(self.step_name)
        file = attach_firearm_certificate["file"]
        return not isinstance(file, CurrentFile)

    def get_firearm_act_certificate_payload(self):
        data = self.wizard.get_cleaned_data_for_step(self.step_name)
        certificate = data["file"]
        payload = {
            **get_document_data(certificate),
            "document_on_organisation": {
                "expiry_date": data["section_certificate_date_of_expiry"].isoformat(),
                "reference_code": data["section_certificate_number"],
                "document_type": self.document_type,
            },
        }
        return payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding firearm certificate when creating firearm",
        "Unexpected error adding firearm certificate",
    )
    def post_firearm_act_certificate(self):
        firearm_certificate_payload = self.get_firearm_act_certificate_payload()
        return post_application_document(
            request=self.request,
            pk=self.application["id"],
            good_pk=self.good["id"],
            data=firearm_certificate_payload,
        )

    def get_organisation_document_payload(self):
        firearm_certificate_cleaned_data = self.wizard.get_cleaned_data_for_step(self.step_name)
        expiry_date = firearm_certificate_cleaned_data["section_certificate_date_of_expiry"]
        reference_code = firearm_certificate_cleaned_data["section_certificate_number"]

        firearm_certificate_payload = {
            "expiry_date": expiry_date.isoformat(),
            "reference_code": reference_code,
            "document_type": self.document_type,
        }
        return firearm_certificate_payload

    @expect_status(
        HTTPStatus.OK,
        "Error updating firearm certificate when editing firearm",
        "Unexpected error updating firearm certificate",
    )
    def update_firearm_act_certificate(self):
        document = get_firearm_act_document(self.application, self.document_type)
        document_payload = self.get_organisation_document_payload()
        return update_document_on_organisation(
            request=self.request,
            organisation_id=document["organisation"],
            document_id=document["id"],
            data=document_payload,
        )

    def run(self):
        if not self.has_firearm_act_certificate():
            return

        if self.is_new_firearm_act_certificate():
            self.post_firearm_act_certificate()
        else:
            self.update_firearm_act_certificate()


class CreateOrUpdateRfdCertificateAction:
    def __init__(self, step_name, wizard):
        self.wizard = wizard
        self.request = wizard.request
        self.application = wizard.application
        self.step_name = step_name

    def has_organisation_rfd_certificate_data(self):
        return bool(self.wizard.get_cleaned_data_for_step(self.step_name))

    def has_existing_certificate(self):
        return has_valid_rfd_certificate(self.application)

    def get_rfd_certificate_payload(self):
        rfd_certificate_cleaned_data = self.wizard.get_cleaned_data_for_step(self.step_name)
        cert_file = rfd_certificate_cleaned_data["file"]
        expiry_date = rfd_certificate_cleaned_data["expiry_date"]
        reference_code = rfd_certificate_cleaned_data["reference_code"]

        rfd_certificate_payload = {
            **get_document_data(cert_file),
            "description": "Registered firearm dealer certificate",
            "document_type": DocumentType.RFD_CERTIFICATE,
            "document_on_organisation": {
                "expiry_date": expiry_date.isoformat(),
                "reference_code": reference_code,
                "document_type": DocumentType.RFD_CERTIFICATE,
            },
        }
        return rfd_certificate_payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error rfd certificate when creating firearm",
        "Unexpected error updating firearm",
    )
    def post_rfd_certificate(self):
        rfd_certificate_payload = self.get_rfd_certificate_payload()
        return post_additional_document(
            request=self.request,
            pk=self.application["id"],
            json=rfd_certificate_payload,
        )

    def has_replacement_file(self):
        attach_rfd_certificate_cleaned_data = self.wizard.get_cleaned_data_for_step(self.step_name)
        file = attach_rfd_certificate_cleaned_data["file"]
        return not isinstance(file, CurrentFile)

    def get_organisation_document_payload(self):
        rfd_certificate_cleaned_data = self.wizard.get_cleaned_data_for_step(self.step_name)
        expiry_date = rfd_certificate_cleaned_data["expiry_date"]
        reference_code = rfd_certificate_cleaned_data["reference_code"]

        rfd_certificate_payload = {
            "expiry_date": expiry_date.isoformat(),
            "reference_code": reference_code,
            "document_type": DocumentType.RFD_CERTIFICATE,
        }
        return rfd_certificate_payload

    @expect_status(
        HTTPStatus.OK,
        "Error updating rfd certificate when creating firearm",
        "Unexpected error updating firearm",
    )
    def update_rfd_certificate(self):
        rfd_document = get_rfd_certificate(self.application)
        rfd_certificate_payload = self.get_organisation_document_payload()
        return update_document_on_organisation(
            request=self.request,
            organisation_id=rfd_document["organisation"],
            document_id=rfd_document["id"],
            data=rfd_certificate_payload,
        )

    def run(self):
        if not self.has_organisation_rfd_certificate_data():
            return

        if not self.has_existing_certificate():
            self.post_rfd_certificate()
            return

        if not self.has_replacement_file():
            self.update_rfd_certificate()
            return
