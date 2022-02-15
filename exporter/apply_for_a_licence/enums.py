from lite_forms.components import Option


class OpenGeneralExportLicenceTypes:
    class OpenGeneralLicenceType:
        def __init__(self, id, name, acronym):
            self.id = id
            self.name = name
            self.acronym = acronym

    open_general_export_licence = OpenGeneralLicenceType(
        "00000000-0000-0000-0000-000000000002", "Open General Export Licence", "OGEL"
    )
    open_general_trade_control_licence = OpenGeneralLicenceType(
        "00000000-0000-0000-0000-000000000013",
        "Open General Trade Control Licence",
        "OGTCL",
    )
    open_general_transhipment_licence = OpenGeneralLicenceType(
        "00000000-0000-0000-0000-000000000014",
        "Open General Transhipment Licence",
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
        return [Option(key=ogl.id, value=f"{ogl.name} ({ogl.acronym})") for ogl in cls.all()]

    @classmethod
    def get_by_acronym(cls, acronym):
        return next(ogl for ogl in cls.all() if ogl.acronym.lower() == acronym.lower())
