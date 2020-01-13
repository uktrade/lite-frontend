from goods.helpers import good_summary
from lite_content.lite_exporter_frontend.goods import AddGoodToApplicationForm
from lite_forms.components import (
    Form,
    HiddenField,
    SideBySideSection,
    Select,
    QuantityInput,
    CurrencyInput,
    RadioButtons,
    Option,
)
from lite_forms.helpers import conditional


def good_on_application_form(good, units):
    return Form(
        title=AddGoodToApplicationForm.TITLE,
        description=AddGoodToApplicationForm.DESCRIPTION,
        questions=[
            conditional(good, good_summary(good)),
            conditional(good, HiddenField(name="good_id", value=good.get("id"))),
            CurrencyInput(
                title=AddGoodToApplicationForm.VALUE.TITLE,
                description=AddGoodToApplicationForm.VALUE.DESCRIPTION,
                name="value",
            ),
            SideBySideSection(
                questions=[
                    QuantityInput(
                        title=AddGoodToApplicationForm.Quantity.TITLE,
                        description=AddGoodToApplicationForm.Quantity.DESCRIPTION,
                        name="quantity",
                    ),
                    Select(
                        title=AddGoodToApplicationForm.Units.TITLE,
                        description=AddGoodToApplicationForm.Units.DESCRIPTION,
                        name="unit",
                        options=units,
                    ),
                ]
            ),
            RadioButtons(
                name="is_good_incorporated",
                title=AddGoodToApplicationForm.Incorporated.TITLE,
                description=AddGoodToApplicationForm.Incorporated.DESCRIPTION,
                options=[
                    Option(True, AddGoodToApplicationForm.Incorporated.YES),
                    Option(False, AddGoodToApplicationForm.Incorporated.NO),
                ],
                classes=["govuk-radios--inline"],
            ),
        ],
        javascript_imports=["/assets/javascripts/add_good.js"],
    )
