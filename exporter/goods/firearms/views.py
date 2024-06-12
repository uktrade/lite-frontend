from core.summaries.summaries import SummaryTypes

from exporter.core.helpers import (
    get_user_organisation_documents,
    has_valid_organisation_rfd_certificate,
)
from exporter.applications.summaries.firearm import firearm_summary, firearm_ammunition_summary

from ..common.base import BaseProductDetails


class FirearmProductDetails(BaseProductDetails):
    summary_type = SummaryTypes.FIREARM

    def get_summary(self):
        is_user_rfd = has_valid_organisation_rfd_certificate(self.organisation)
        organisation_documents = get_user_organisation_documents(self.organisation)
        return firearm_summary(
            self.good,
            is_user_rfd,
            organisation_documents,
        )

class FirearmAmmunitionProductDetails(BaseProductDetails):
    summary_type = SummaryTypes.FIREARM_AMMUNITION

    def get_summary(self):
        is_user_rfd = has_valid_organisation_rfd_certificate(self.organisation)
        organisation_documents = get_user_organisation_documents(self.organisation)
        return firearm_ammunition_summary(
            self.good,
            is_user_rfd,
            organisation_documents,
        )
