from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import F680Questions
from lite_forms.components import FormGroup, Form, RadioButtons, Option, TextArea, DateInput, CurrencyInput, Label


def questions_forms():
    return FormGroup(
        [
            expedited_form(),
            foreign_technology_form(),
            locally_manufactured_form(),
            mtcr_form(),
            electronic_warfare_form(),
            uk_service_equipment_form(),
            uk_service_equipment_type_form(),
            prospect_value_form(),
        ],
    )


def expedited_form():
    return Form(
        caption=F680Questions.CAPTION,
        title=F680Questions.Expedited.TITLE,
        questions=[
            RadioButtons(
                name="expedited",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[DateInput(title=F680Questions.Expedited.DATE, name="expedited_date", prefix=""),],
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
                name="foreign_technology",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=F680Questions.ForeignTechnology.PROVIDE_DETAILS,
                                name="foreign_technology_description",
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
                name="locally_manufactured",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=F680Questions.LocallyManufactured.PROVIDE_DETAILS,
                                name="locally_manufactured_description",
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
                name="mtcr_type",
                options=[
                    Option(key="mtcr_category_1", value=F680Questions.MtcrType.Categories.ONE),
                    Option(key="mtcr_category_2", value=F680Questions.MtcrType.Categories.TWO),
                    Option(key="none", value=F680Questions.MtcrType.Categories.NO),
                    Option(key="unknown", value=F680Questions.MtcrType.Categories.I_DONT_KNOW, show_or=True),
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
                name="electronic_warfare_requirement",
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
                name="uk_service_equipment",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=F680Questions.UKServiceEquipment.PROVIDE_DETAILS_OPTIONAL,
                                name="uk_service_equipment_description",
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
                name="uk_service_equipment_type",
                options=[
                    Option(key="mod_funded", value=F680Questions.UKServiceEquipment.Types.MOD_FUNDED),
                    Option(
                        key="part_mod_part_venture", value=F680Questions.UKServiceEquipment.Types.MOD_VENTURE_FUNDED
                    ),
                    Option(key="private_venture", value=F680Questions.UKServiceEquipment.Types.PRIVATE_VENTURE),
                ],
            ),
        ],
    )


def prospect_value_form():
    return Form(
        caption=F680Questions.CAPTION,
        title=F680Questions.ProspectValue.TITLE,
        questions=[CurrencyInput(name="prospect_value")],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )
