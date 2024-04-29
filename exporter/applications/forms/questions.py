from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import F680Questions
from lite_forms.components import FormGroup, Form, RadioButtons, Option, TextArea, CurrencyInput, Label


def f680_questions_forms():
    return FormGroup(
        [
            expedited_form(),
            foreign_technology_form(),
            locally_manufactured_form(),
            mtcr_form(),
            electronic_warfare_form(),
            uk_service_equipment_form(),
            uk_service_equipment_type_form(),
        ],
    )


def oiel_questions_forms():
    return FormGroup(
        [
            nature_of_product_form(),
            number_of_siels_last_year(),
            purely_commercial(),
        ],
    )


def nature_of_product_form():
    return Form(
        caption="OIEL Additional information",
        title='Can you please provide a general description of the nature of the products you are intending to export, including how you have assessed them against the control entries specified in "Items authorised to be exported" on the application form.',
        questions=[
            TextArea(
                title="",
                name="nature_of_product",
                description="",
                extras={"max_length": 2200},
                optional=False,
            ),
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def number_of_siels_last_year():
    return Form(
        caption="OIEL Additional information",
        title="Can you please provide the number of SIELs you have obtained in the last 12 months and to which destinations.",
        questions=[
            TextArea(
                title="",
                name="number_of_siels_last_year",
                description="",
                extras={"max_length": 2200},
                optional=False,
            ),
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def purely_commercial():
    return Form(
        caption="OIEL Additional information",
        title="Can you please confirm that your customers are purely commercial (ie: this Cryptographic OIEL cannot be used if your items are being exported for Government or military end use).",
        questions=[
            RadioButtons(
                name="purely_commercial",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def expedited_form():
    return Form(
        caption=F680Questions.CAPTION,
        title=F680Questions.Expedited.TITLE,
        questions=[
            RadioButtons(
                name="exceptional_circumstances",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def foreign_technology_form():
    return Form(
        caption=F680Questions.CAPTION,
        title=F680Questions.ForeignTechnology.TITLE,
        questions=[
            RadioButtons(
                name="foreign_technology_information",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=F680Questions.ForeignTechnology.PROVIDE_DETAILS,
                                name="foreign_technology_information_details",
                                description=F680Questions.ForeignTechnology.DESCRIPTION,
                                extras={"max_length": 2200},
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def locally_manufactured_form():
    return Form(
        caption=F680Questions.CAPTION,
        title=F680Questions.LocallyManufactured.TITLE,
        questions=[
            RadioButtons(
                name="is_local_assembly_manufacture",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=F680Questions.LocallyManufactured.PROVIDE_DETAILS,
                                name="is_local_assembly_manufacture_details",
                                extras={"max_length": 2200},
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def mtcr_form():
    return Form(
        caption=F680Questions.CAPTION,
        title=F680Questions.MtcrType.TITLE,
        questions=[
            RadioButtons(
                name="product_mtcr_rating_type",
                options=[
                    Option(key="YES_MTCR_CAT1", value=F680Questions.MtcrType.Categories.ONE),
                    Option(key="YES_MTCR_CAT2", value=F680Questions.MtcrType.Categories.TWO),
                    Option(key="NO", value=F680Questions.MtcrType.Categories.NO),
                    Option(key="DONT_KNOW", value=F680Questions.MtcrType.Categories.I_DONT_KNOW, show_or=True),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def electronic_warfare_form():
    return Form(
        caption=F680Questions.CAPTION,
        title=F680Questions.EWRequirement.TITLE,
        questions=[
            RadioButtons(
                name="ew_data",
                options=[
                    Option(key=True, value="Yes", components=[Label(text=F680Questions.EWRequirement.ATTACHMENT)]),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def uk_service_equipment_form():
    return Form(
        caption=F680Questions.CAPTION,
        title=F680Questions.UKServiceEquipment.TITLE,
        questions=[
            RadioButtons(
                name="armed_forces_usage",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=F680Questions.UKServiceEquipment.PROVIDE_DETAILS_OPTIONAL,
                                name="armed_forces_usage_details",
                                extras={"max_length": 2200},
                            )
                        ],
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def uk_service_equipment_type_form():
    return Form(
        caption=F680Questions.CAPTION,
        title=F680Questions.UKServiceEquipment.TYPE,
        questions=[
            RadioButtons(
                name="product_funding",
                options=[
                    Option(key="MOD", value=F680Questions.UKServiceEquipment.Types.MOD_FUNDED),
                    Option(key="PART_MOD", value=F680Questions.UKServiceEquipment.Types.MOD_VENTURE_FUNDED),
                    Option(key="PRIVATE_VENTURE", value=F680Questions.UKServiceEquipment.Types.PRIVATE_VENTURE),
                ],
            ),
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def prospect_value_form():
    return Form(
        caption=F680Questions.CAPTION,
        title=F680Questions.ProspectValue.TITLE,
        questions=[CurrencyInput(name="prospect_value")],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )
