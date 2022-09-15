from core.summaries.summaries import SummaryTypes

from exporter.applications.summaries.software import software_summary

from ..common.base import BaseProductDetails


class SoftwareProductDetails(BaseProductDetails):
    summary_type = SummaryTypes.SOFTWARE

    def get_summary(self):
        return software_summary(self.good)
