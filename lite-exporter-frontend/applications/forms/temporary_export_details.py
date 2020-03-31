from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import TemporaryExportDetails
from lite_forms.components import FormGroup, TextArea, Form, RadioButtons, Option, DateInput


def temporary_export_details_form():
    return FormGroup(
        [
            provide_export_details_form(TemporaryExportDetails.TEMPORARY_EXPORT_DETAILS_CAPTION),
            is_temp_direct_control_form(TemporaryExportDetails.TEMPORARY_EXPORT_DETAILS_CAPTION),
            proposed_product_return_date_form(TemporaryExportDetails.TEMPORARY_EXPORT_DETAILS_CAPTION),
        ]
    )


def provide_export_details_form(caption):
    return Form(
        caption=caption,
        title=TemporaryExportDetails.TEMPORARY_EXPORT_DETAILS,
        questions=[
            TextArea(
                name="temp_export_details",
                short_title=TemporaryExportDetails.SummaryList.TEMPORARY_EXPORT_DETAILS,
                extras={"max_length": 2200},
                optional=False,
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def is_temp_direct_control_form(caption):
    return Form(
        caption=caption,
        title=TemporaryExportDetails.PRODUCTS_UNDER_DIRECT_CONTROL,
        questions=[
            RadioButtons(
                name="is_temp_direct_control",
                short_title=TemporaryExportDetails.SummaryList.PRODUCTS_UNDER_DIRECT_CONTROL,
                options=[
                    Option(key=True, value="Yes"),
                    Option(
                        key=False,
                        value="No",
                        components=[
                            TextArea(
                                name="temp_direct_control_details",
                                title=TemporaryExportDetails.PRODUCTS_UNDER_DIRECT_CONTROL_DETAILS,
                                description="",
                                extras={"max_length": 2200},
                                optional=False,
                            )
                        ],
                    ),
                ],
                classes=["govuk-radios--inline"],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def proposed_product_return_date_form(caption):
    return Form(
        caption=caption,
        title=TemporaryExportDetails.PROPOSED_RETURN_DATE,
        questions=[
            DateInput(
                title="",
                short_title=TemporaryExportDetails.SummaryList.PROPOSED_RETURN_DATE,
                description=TemporaryExportDetails.PROPOSED_DATE_HINT,
                name="proposed_return_date",
                prefix="",
                optional=False,
            ),
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )
