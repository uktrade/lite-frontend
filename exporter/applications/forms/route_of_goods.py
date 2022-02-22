from exporter.core.constants import CONTINUE, RouteOfGoods
from lite_forms.components import Form, Option, TextArea, RadioButtons, BackLink, HiddenField, HTMLBlock


def route_of_goods_form(back_link):
    return Form(
        title=RouteOfGoods.TITLE,
        back_link=BackLink("Back", back_link),
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
                + "<a class='govuk-link' "
                + "href='https://www.great.gov.uk/advice/prepare-for-export-procedures-and-logistics/understand-international-trade-terms/'>"
                + "Understand international trade terms</a>"
                + "</div>"
                + "</details>"
                "<br>"
            ),
        ],
        default_button_name=CONTINUE,
    )
