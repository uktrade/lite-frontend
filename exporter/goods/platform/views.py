from core.summaries.summaries import SummaryTypes

from exporter.applications.summaries.platform import complete_item_summary

from ..common.base import BaseProductDetails


class PlatformProductDetails(BaseProductDetails):
    summary_type = SummaryTypes.COMPLETE_ITEM

    def get_summary(self):
        return complete_item_summary(self.good)
