from munch import Munch

from cases.constants import CaseType
from conf.constants import GoodsTypeCategory


class Slice:
    def __init__(self, file, title=None):
        self.file = file
        self.title = title


class Case(Munch):
    @property
    def data(self):
        if "application" in self:
            return self["application"]
        else:
            return self["query"]

    @property
    def organisation(self):
        return self.data["organisation"]

    @property
    def status(self):
        return self.data["status"]["key"]

    @property
    def type(self):
        return self["case_type"]["type"]["key"]

    @property
    def sub_type(self):
        return self["case_type"]["sub_type"]["key"]

    @property
    def goods(self):
        if "goods" not in self.data and "goods_types" not in self.data:
            return []

        return self.data.get("goods", self.data.get("goods_types"))

    @property
    def destinations(self):
        if "destinations" not in self.data:
            return []

        destinations = self.data["destinations"]["data"]

        # Some apps return just the end user (as type dict) in destinations,
        # so we need to add the other destinations
        if isinstance(destinations, dict):
            destinations = [destinations]
            if self.data.get("consignee"):
                destinations.append(self.data.get("consignee"))
            if self.data.get("ultimate_end_users"):
                destinations += self.data.get("ultimate_end_users")
            if self.data.get("third_parties"):
                destinations += self.data.get("third_parties")

        return destinations

    @property
    def open_app_parties(self):
        parties = []
        if self.data["case_type"]["sub_type"]["key"] == CaseType.OPEN.value:
            if self.data.get("end_user"):
                parties.append(self.data.get("end_user"))
            if (
                self.data.get("ultimate_end_users")
                and self.data["goodstype_category"]["key"] == GoodsTypeCategory.MILITARY
            ):
                parties.extend(self.data.get("ultimate_end_users"))

        return parties

    @property
    def case_officer(self):
        if self["case_officer"]:
            return self["case_officer"]
        else:
            return {}
