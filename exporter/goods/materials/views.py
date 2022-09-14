from exporter.applications.summaries.material import material_summary

from ..common.base import BaseProductDetails


class MaterialProductDetails(BaseProductDetails):
    def get_summary(self):
        return material_summary(self.good)
