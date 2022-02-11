import datetime

from exporter.core.constants import TemporaryExportDetails
from lite_content.lite_exporter_frontend import generic
from lite_forms.components import FormGroup, TextArea, Form, RadioButtons, Option, DateInput, BackLink


def temporary_export_details_form(back_link_url):
    return FormGroup(
        [
            provide_export_details_form(back_link_url=back_link_url),
            is_temp_direct_control_form(),
            proposed_product_return_date_form(),
        ]
    )


def provide_export_details_form(back_link_url):
    return Form(
        back_link=BackLink("Back", back_link_url),
        title=TemporaryExportDetails.TEMPORARY_EXPORT_DETAILS,
        questions=[
            TextArea(
                name="temp_export_details",
                short_title=TemporaryExportDetails.SummaryList.TEMPORARY_EXPORT_DETAILS,
                optional=False,
                rows=5,
            )
        ],
        default_button_name=generic.CONTINUE,
    )


def is_temp_direct_control_form():
    return Form(
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
                                optional=False,
                                rows=5,
                            )
                        ],
                    ),
                ],
                classes=["govuk-radios--inline"],
            )
        ],
        default_button_name=generic.CONTINUE,
    )


def proposed_product_return_date_form():
    return Form(
        title=TemporaryExportDetails.PROPOSED_RETURN_DATE,
        questions=[
            DateInput(
                title="",
                short_title=TemporaryExportDetails.SummaryList.PROPOSED_RETURN_DATE,
                description=f"For example, 12 11 {datetime.datetime.now().year + 1}",
                name="proposed_return_date",
                prefix="",
                optional=False,
            ),
        ],
        default_button_name=generic.CONTINUE,
    )
