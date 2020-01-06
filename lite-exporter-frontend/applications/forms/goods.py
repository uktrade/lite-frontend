from goods.helpers import good_summary
from lite_content.lite_exporter_frontend import strings
from lite_forms.components import Form, HiddenField, SideBySideSection, Select, QuantityInput, CurrencyInput
from lite_forms.helpers import conditional


def good_on_application_form(good, units, title, prefix=""):
    return Form(
        title=title,
        questions=[
            conditional(good, good_summary(good)),
            conditional(good, HiddenField(name="good_id", value=good.get("id"))),
            CurrencyInput(title=strings.goods.CreateGoodOnApplicationForm.VALUE, name=prefix + "value"),
            SideBySideSection(
                questions=[
                    QuantityInput(title=strings.goods.CreateGoodOnApplicationForm.QUANTITY, name=prefix + "quantity"),
                    Select(title=strings.goods.CreateGoodOnApplicationForm.UNITS, name=prefix + "unit", options=units),
                ]
            ),
        ],
        javascript_imports=["/assets/javascripts/specific/add_good.js"],
    )
