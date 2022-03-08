import datetime

from exporter.core.constants import (
    CONTINUE,
    GoodsRecipients,
    GoodsStartingPoint,
    PERMANENT,
    RouteOfGoods,
    TEMPORARY,
    TemporaryExportDetails,
    TemporaryOrPermanent,
)
from lite_forms.components import (
    FormGroup,
    TextArea,
    Form,
    RadioButtons,
    Option,
    DateInput,
    BackLink,
    HiddenField,
    HTMLBlock,
)
from lite_forms.helpers import conditional


def export_details_form(back_link_url, is_temporary):
    return FormGroup(
        [
            goods_starting_point_form(back_link_url=back_link_url),
            permanent_temporary_export_form(),
            conditional(is_temporary, provide_export_details_form()),
            conditional(is_temporary, is_temp_direct_control_form()),
            conditional(is_temporary, proposed_product_return_date_form()),
            route_of_goods_form(),
            goods_recipients_form(),
        ]
    )


def goods_starting_point_form(back_link_url):
    return Form(
        back_link=BackLink("Back", back_link_url),
        title=GoodsStartingPoint.TITLE,
        questions=[
            RadioButtons(
                name="goods_starting_point",
                short_title=GoodsStartingPoint.TITLE,
                options=[
                    Option(
                        key="GB",
                        value="Great Britain",
                    ),
                    Option(
                        key="NI",
                        value="Northern Ireland",
                    ),
                ],
            )
        ],
        default_button_name=CONTINUE,
    )


def permanent_temporary_export_form():
    return Form(
        title=TemporaryOrPermanent.TITLE,
        questions=[
            RadioButtons(
                name="export_type",
                short_title=TemporaryOrPermanent.TITLE,
                options=[
                    Option(
                        key=PERMANENT,
                        value=TemporaryOrPermanent.YES,
                    ),
                    Option(
                        key=TEMPORARY,
                        value=TemporaryOrPermanent.NO,
                    ),
                ],
            )
        ],
        default_button_name=CONTINUE,
    )


def provide_export_details_form():
    return Form(
        title=TemporaryExportDetails.TEMPORARY_EXPORT_DETAILS,
        questions=[
            TextArea(
                name="temp_export_details",
                short_title=TemporaryExportDetails.SummaryList.TEMPORARY_EXPORT_DETAILS,
                optional=False,
                rows=5,
            )
        ],
        default_button_name=CONTINUE,
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
        default_button_name=CONTINUE,
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
        default_button_name=CONTINUE,
    )


def route_of_goods_form():
    return Form(
        title=RouteOfGoods.TITLE,
        questions=[
            RadioButtons(
                name="is_shipped_waybill_or_lading",
                short_title="",
                options=[
                    Option(key=True, value="Yes"),
                    Option(
                        key=False,
                        value="No",
                        components=[
                            TextArea(
                                name="non_waybill_or_lading_route_details",
                                title="",
                                description=RouteOfGoods.NO_ANSWER_DESCRIPTION,
                                optional=False,
                                rows=5,
                            )
                        ],
                    ),
                ],
                classes=["govuk-radios--inline"],
            ),
            HiddenField("section_certificate_step", True),
            HTMLBlock(
                "<br>"
                + "<details class='govuk-details' data-module='govuk-details'>"
                + "<summary class='govuk-details__summary'>"
                + "<span class='govuk-details__summary-text'>Help with airway bill and bill of landing</span>"
                + "</summary>"
                + "<div class='govuk-details__text govuk'>"
                + "<p>"
                + "An air waybill is a receipt issued by an international airline for goods, and evidence of the contract of carriage. "
                + "It obliges the carrier to carry the goods to the airport of destination, according to specified conditions. "
                + "It is a document of title, which proves ownership, and is non-negotiable."
                + "</p>"
                + "<p>"
                + "A bill of lading is a contract between the owner of the goods and the carrier. It is a receipt, "
                + "contains the terms of the carriage contract, and importantly, is a document of title, which proves ownership of the goods."
                + "</p>"
                + "<a class='govuk-link' target='_blank' "
                + "href='https://www.great.gov.uk/advice/prepare-for-export-procedures-and-logistics/understand-international-trade-terms/'>"
                + "Understand international trade terms</a>"
                + "</div>"
                + "</details>"
                "<br>"
            ),
        ],
        default_button_name=CONTINUE,
    )


def goods_recipients_form():
    return Form(
        title=GoodsRecipients.TITLE,
        questions=[
            RadioButtons(
                name="goods_recipients",
                short_title="",
                options=[
                    Option(key="direct_to_end_user", value="Directly to the end-user"),
                    Option(key="via_consignee", value="To an end-user via a consignee"),
                    Option(
                        key="via_consignee_and_third_parties",
                        value="To an end-user via a consignee, with additional third parties",
                    ),
                ],
            ),
            HiddenField("section_certificate_step", True),
            HTMLBlock(
                "<br>"
                + "<details class='govuk-details' data-module='govuk-details'>"
                + "<summary class='govuk-details__summary'>"
                + "<span class='govuk-details__summary-text'>Help with end user, consignee and third party</span>"
                + "</summary>"
                + "<div class='govuk-details__text govuk'>"
                + "<p>An end-user receives the products in the destination country. They either use the products "
                + "themselves, resell from stock, or export them again to another country.</p>"
                + "<p>A consignee receives the products and then delivers or sells them to the end-user.</p>"
                + "<p>A third party is involved in the export but not regarded as a consignee, end-user or ultimate "
                + "end-user, for example they might be an agent, broker, consultant or distributor.</p>"
                + "<p>For products being exported again passed their first destination, there may also be an ultimate "
                + "end-user. An ultimate end-user in a third country receives goods via an onward export from the end user.</p>"
                + "</div>"
                + "</details>"
                "<br>"
            ),
        ],
        default_button_name=CONTINUE,
    )
