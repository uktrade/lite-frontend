from core.summaries.summaries import SummaryTypes

from exporter.applications.summaries.component import component_accessory_summary

from ..common.base import BaseProductDetails


class ComponentAccessoryProductDetails(BaseProductDetails):
    summary_type = SummaryTypes.COMPONENT_ACCESSORY

    def get_summary(self):
        return component_accessory_summary(self.good)
