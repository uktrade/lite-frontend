from lite_content.lite_internal_frontend.open_general_licences import (
    OGEL_DESCRIPTION,
    OGTCL_DESCRIPTION,
    OGTL_DESCRIPTION,
)
from lite_forms.components import Option


class OpenGeneralExportLicences:
    class OpenGeneralLicence:
        def __init__(self, id, name, description, acronym):
            self.id = id
            self.name = name
            self.description = description
            self.acronym = acronym

    open_general_export_licence = OpenGeneralLicence(
        "00000000-0000-0000-0000-000000000002",
        "Open General Export Licence",
        OGEL_DESCRIPTION,
        "OGEL",
    )
    open_general_trade_control_licence = OpenGeneralLicence(
        "00000000-0000-0000-0000-000000000013",
        "Open General Trade Control Licence",
        OGTCL_DESCRIPTION,
        "OGTCL",
    )
    open_general_transhipment_licence = OpenGeneralLicence(
        "00000000-0000-0000-0000-000000000014",
        "Open General Transhipment Licence",
        OGTL_DESCRIPTION,
        "OGTL",
    )

    @classmethod
    def all(cls):
        return [
            cls.open_general_export_licence,
            cls.open_general_trade_control_licence,
            cls.open_general_transhipment_licence,
        ]

    @classmethod
    def as_options(cls):
        return [
            Option(key=ogl.id, value=f"{ogl.name} ({ogl.acronym})", description=ogl.description) for ogl in cls.all()
        ]

    @classmethod
    def get_by_id(cls, id):
        return next(ogl for ogl in cls.all() if ogl.id == id)
