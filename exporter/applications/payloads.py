from core.wizard.payloads import (
    get_cleaned_data,
    MergingPayloadBuilder,
)

from exporter.applications.constants import ExportLicenceSteps


class ExportLicencePayloadBuilder(MergingPayloadBuilder):
    payload_dict = {
        ExportLicenceSteps.LICENCE_TYPE: get_cleaned_data,
        ExportLicenceSteps.APPLICATION_NAME: get_cleaned_data,
        ExportLicenceSteps.TOLD_BY_AN_OFFICIAL: get_cleaned_data,
    }

    def build(self, form_dict):
        payload = super().build(form_dict)

        payload.update(
            {
                "application_type": "siel",
                "export_type": "permanent",
            }
        )

        return payload
