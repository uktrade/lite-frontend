from core.summaries.summaries import SummaryTypes

from exporter.applications.summaries.material import material_summary

from ..common.base import BaseProductDetails


class MaterialProductDetails(BaseProductDetails):
    summary_type = SummaryTypes.MATERIAL

    def get_summary(self):
        return material_summary(self.good)
