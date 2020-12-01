from django.urls import reverse_lazy

from exporter.core.constants import EXHIBITION
from exporter.core.services import get_units, get_item_types
from exporter.goods.helpers import good_summary
from exporter.goods.forms import identification_markings_form
from lite_content.lite_exporter_frontend import strings
from lite_content.lite_exporter_frontend.goods import AddGoodToApplicationForm
from lite_forms.components import (
    Form,
    FormGroup,
    HiddenField,
    Select,
    QuantityInput,
    CurrencyInput,
    RadioButtons,
    Option,
    BackLink,
)


def exhibition_item_type(request, good_id, application_id):
    return Form(
        title=AddGoodToApplicationForm.Exhibition.TITLE,
        description=AddGoodToApplicationForm.Exhibition.DESCRIPTION,
        questions=[
            HiddenField(name="good_id", value=good_id),
            RadioButtons(title="", description="", name="item_type", options=get_item_types(request)),
        ],
        back_link=BackLink(
            AddGoodToApplicationForm.Exhibition.BACK_LINK,
            reverse_lazy("applications:preexisting_good", kwargs={"pk": application_id}),
        ),
    )


def good_unit_value_and_quantity(request, good, sub_case_type, application_id):
    if sub_case_type["key"] == EXHIBITION:
        return exhibition_item_type(request, good.get("id"), application_id)
    else:
        return Form(
            title=AddGoodToApplicationForm.TITLE,
            description=AddGoodToApplicationForm.DESCRIPTION,
            questions=[
                good_summary(good),
                HiddenField(name="good_id", value=good.get("id")),
                Select(
                    title=AddGoodToApplicationForm.Units.TITLE,
                    description="<noscript>" + AddGoodToApplicationForm.Units.DESCRIPTION + "</noscript>",
                    name="unit",
                    options=get_units(request),
                ),
                QuantityInput(
                    title=AddGoodToApplicationForm.Quantity.TITLE,
                    description=AddGoodToApplicationForm.Quantity.DESCRIPTION,
                    name="quantity",
                ),
                CurrencyInput(
                    title=AddGoodToApplicationForm.VALUE.TITLE,
                    description=AddGoodToApplicationForm.VALUE.DESCRIPTION,
                    name="value",
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
            back_link=BackLink(
                strings.BACK_TO_APPLICATION,
                reverse_lazy("applications:preexisting_good", kwargs={"pk": application_id}),
            ),
            javascript_imports={"/javascripts/add-good.js"},
        )


def good_on_application_form_group(request, good, sub_case_type, draft_pk):
    return FormGroup(
        [identification_markings_form(draft_pk), good_unit_value_and_quantity(request, good, sub_case_type, draft_pk),]
    )
