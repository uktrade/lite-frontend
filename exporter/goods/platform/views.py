from exporter.applications.summaries.platform import platform_summary

from ..common.base import BaseProductDetails


class PlatformProductDetails(BaseProductDetails):
    def get_summary(self):
        return platform_summary(self.good)
