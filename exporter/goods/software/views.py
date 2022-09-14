from exporter.applications.summaries.software import software_summary

from ..common.base import BaseProductDetails


class SoftwareProductDetails(BaseProductDetails):
    def get_summary(self):
        return software_summary(self.good)
