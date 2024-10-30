from django.urls import reverse_lazy

from exporter.core.constants import CaseTypes
from exporter.core.services import get_trade_control_activities, get_trade_control_product_categories
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.applications import TradeControlLicenceQuestions
from lite_forms.components import Form, RadioButtons, Option, BackLink, TextArea, Checkboxes


def application_type_form():
    return Form(
        title=TradeControlLicenceQuestions.TradeControlLicenceQuestion.TITLE,
        description="",
        questions=[
            RadioButtons(
                name="application_type",
                options=[
                    Option(
                        key=CaseTypes.OGTCL,
                        value=TradeControlLicenceQuestions.TradeControlLicenceQuestion.OPEN_GENERAL_TRADE_CONTROL_LICENCE,
                        description=(
                            "Select to register a pre-published licence with set terms and conditions. "
                            "Being an OGTCL holder can benefit your business by saving time and money."
                        ),
                    ),
                    Option(
                        key=CaseTypes.SICL,
                        value=TradeControlLicenceQuestions.TradeControlLicenceQuestion.STANDARD_LICENCE,
                        description="Select a standard licence for a set quantity and set value of products.",
                    ),
                    Option(
                        key=CaseTypes.OICL,
                        value=TradeControlLicenceQuestions.TradeControlLicenceQuestion.OPEN_LICENCE,
                        description=(
                            "Select an open licence for multiple shipments of specific products to specific destinations. "
                            "Open licences cover long term projects and repeat business."
                        ),
                    ),
                ],
            )
        ],
        default_button_name=generic.CONTINUE,
        back_link=BackLink(
            TradeControlLicenceQuestions.TradeControlLicenceQuestion.BACK, reverse_lazy("apply_for_a_licence:start")
        ),
    )


def activity_form(request):
    activities = get_trade_control_activities(request)
    options = []

    for activity in activities:
        option = Option(activity["key"], activity["value"])

        if activity["key"] == "other":
            option.components = [
                TextArea(
                    title=TradeControlLicenceQuestions.ControlActivity.OTHER_DESCRIPTION,
                    name="trade_control_activity_other",
                    optional=False,
                    rows=1,
                    extras={"max_length": 100},
                )
            ]

        options.append(option)

    return Form(
        title=TradeControlLicenceQuestions.ControlActivity.TITLE,
        description="",
        questions=[RadioButtons(name="trade_control_activity", options=options)],
        default_button_name=generic.CONTINUE,
    )


def product_category_form(request):
    product_categories = get_trade_control_product_categories(request)
    hint_text_map = {
        "category_a": TradeControlLicenceQuestions.ProductCategory.CATEGORY_A_HINT,
        "category_b": TradeControlLicenceQuestions.ProductCategory.CATEGORY_B_HINT,
        "category_c": TradeControlLicenceQuestions.ProductCategory.CATEGORY_C_HINT,
    }
    guidence_url = "https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology#trade-controls-and-arranging-sales-or-movements"
    PRODUCT_CATEGORY_DESCRIPTION = (
        'Find out about <a class="govuk-link govuk-link--no-visited-state" '
        f'rel="noreferrer noopener" target="_blank" href="{guidence_url}">'
        "trade control product categories</a>."
    )

    options = [
        Option(product_category["key"], product_category["value"], hint_text_map.get(product_category["key"]))
        for product_category in product_categories
    ]
    return Form(
        title=TradeControlLicenceQuestions.ProductCategory.TITLE,
        description=PRODUCT_CATEGORY_DESCRIPTION,
        questions=[Checkboxes(name="trade_control_product_categories[]", options=options)],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )
