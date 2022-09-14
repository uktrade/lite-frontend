from exporter.applications.summaries.component import component_summary

from ..common.base import BaseProductDetails


class ComponentProductDetails(BaseProductDetails):
    def get_summary(self):
        return component_summary(self.good)
