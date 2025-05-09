from munch import Munch

from exporter.core.constants import APPLICANT_EDITING
from core.builtins.custom_tags import str_date
from core.application_manifests.contants import ServiceType
from core.application_manifests.registry import application_manifest_registry


class Tab:
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url


class Application(Munch):
    @property
    def manifest(self):
        return application_manifest_registry.get_manifest(ServiceType.EXPORTER.value, self.type)

    @property
    def type_reference(self):
        return self["case_type"]["reference"]["key"]

    @property
    def type_reference_value(self):
        return self["case_type"]["reference"]["value"]

    @property
    def sub_type(self):
        return self["case_type"]["sub_type"]["key"]

    @property
    def type(self):
        return self["case_type"]["type"]["key"]

    @property
    def sub_type_value(self):
        return self["case_type"]["sub_type"]["value"]

    @property
    def status(self):
        # Status can sometime be null, hence use a get
        return self["status"].get("key")

    @property
    def created_at(self):
        return str_date(self["created_at"])

    @property
    def submitted_at(self):
        return str_date(self["submitted_at"])

    def is_editable(self):
        if self.status:
            is_editing = self.status == "submitted" or self.status == APPLICANT_EDITING
            if is_editing:
                return self.status == "submitted"

    def is_major_editable(self):
        if self.status:
            is_editing = self.status == "submitted" or self.status == APPLICANT_EDITING
            if is_editing:
                return self.status != "submitted"

    @property
    def is_eu_military(self):
        return self.get("is_eu_military", False)

    @property
    def intended_end_use(self):
        return self.get("intended_end_use", None)

    @property
    def licence(self):
        return self.get("licence")
