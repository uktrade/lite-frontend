from http import HTTPStatus

from exporter.applications.services import post_application_document
from exporter.core.helpers import get_document_data

from .decorators import expect_status


class PostFirearmActCertificateAction:
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

    def run(self):
        if not self.has_firearm_act_certificate():
            return

        self.post_firearm_act_certificate()
