from core.summaries.summaries import SummaryTypes

from exporter.applications.summaries.software import technology_summary

from ..common.base import BaseProductDetails


class TechnologyProductDetails(BaseProductDetails):
    summary_type = SummaryTypes.TECHNOLOGY

    def get_summary(self):
        return technology_summary(self.good)
