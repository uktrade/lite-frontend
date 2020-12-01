from django.urls import reverse_lazy

from exporter.core.constants import EXHIBITION, PRODUCT_CATEGORY_FIREARM
from exporter.core.services import get_units, get_item_types
from exporter.goods.helpers import good_summary
from lite_content.lite_exporter_frontend import strings
from lite_content.lite_exporter_frontend.goods import AddGoodToApplicationForm
from lite_forms.components import (
    Form,
    HiddenField,
    Select,
    QuantityInput,
    CurrencyInput,
    RadioButtons,
    Option,
    BackLink,
    TextArea,
    DateInput,
)


def exhibition_good_on_application_form(request, good_id, application_id):
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


def good_on_application_form(request, good, sub_case_type, application_id):
    if sub_case_type["key"] == EXHIBITION:
        return exhibition_good_on_application_form(request, good.get("id"), application_id)
    else:
        questions = [
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
        ]

        if good["item_category"]["key"] == PRODUCT_CATEGORY_FIREARM:
            firearm_type = good["firearm_details"]["type"]["key"]
            if firearm_type in ["ammunition", "firearms"]:
                questions.append(firearm_proof_mark_field())
            elif firearm_type == "components_for_firearms":
                questions.append(does_firearm_component_require_proof_marks_field())
            if firearm_type == "firearms":
                questions.append(firearm_is_deactivated_field())

        return Form(
            title=AddGoodToApplicationForm.TITLE,
            description=AddGoodToApplicationForm.DESCRIPTION,
            questions=questions,
            back_link=BackLink(
                strings.BACK_TO_APPLICATION,
                reverse_lazy("applications:preexisting_good", kwargs={"pk": application_id}),
            ),
            javascript_imports={"/javascripts/add-good.js"},
        )


def does_firearm_component_require_proof_marks_field():
    return RadioButtons(
        title="Is the product a gun barrel or the action of a gun?",
        name="is_gun_barrel",
        options=[
            Option(key=True, value="Yes", components=[firearm_proof_mark_field()],),
            Option(key=False, value="No"),
        ],
    )


def firearm_proof_mark_field():
    return RadioButtons(
        title="Does the product have valid UK proof marks?",
        name="has_proof_mark",
        options=[
            Option(key=True, value="Yes"),
            Option(
                key=False,
                value="No",
                components=[
                    TextArea(
                        title="Please give details why not",
                        description="",
                        name="no_proof_mark_details",
                        optional=False,
                    ),
                ],
            ),
        ],
    )


def firearm_is_deactivated_field():
    return RadioButtons(
        title="Has the product been deactivated?",
        name="is_deactivated",
        options=[
            Option(
                key=True,
                value="Yes",
                components=[
                    DateInput(
                        title='Date of deactivation',
                        name="date_of_deactivation",
                        prefix='date_of_deactivation',
                    ),
                    RadioButtons(
                        title="Has the product been deactivated to UK/EU proof house standards?",
                        name="is_deactivated_to_standard",
                        options=[
                            Option(
                                key=True,
                                value="Yes",
                                components=[
                                    Select(
                                        title='Proof house standard',
                                        name="deactivation_standard",
                                        options=[Option(key='UK', value="UK"), Option(key='EU', value="EU"),],
                                    ),
                                ]
                            ),
                            Option(
                                key=False,
                                value="No",
                                components=[
                                    TextArea(
                                        title="Describe who deactivated the product and to what standard it was done",
                                        description="",
                                        name="deactivation_standard_other",
                                        optional=False,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            Option(key=False, value="No"),
        ],
    )
