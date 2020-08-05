from lite_content.lite_exporter_frontend.applications import RouteOfGoods
from lite_forms.components import Form, Option, TextArea, RadioButtons


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
                                extras={"max_length": 2000},
                                optional=False,
                            )
                        ],
                    ),
                ],
                classes=["govuk-radios--inline"],
            )
        ],
        default_button_name=RouteOfGoods.SAVE_BUTTON,
    )
