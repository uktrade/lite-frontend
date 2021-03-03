from django.urls import reverse_lazy

from exporter.core.constants import EXHIBITION, PRODUCT_CATEGORY_FIREARM, FIREARM_AMMUNITION_COMPONENT_TYPES
from exporter.core.services import get_units, get_item_types
from exporter.goods.helpers import good_summary
from exporter.goods.forms import (
    firearms_number_of_items,
    identification_markings_form,
    firearms_capture_serial_numbers,
    firearm_year_of_manufacture_details_form,
    firearms_act_confirmation_form,
    attach_firearm_dealer_certificate_form,
    is_registered_firearm_dealer_field,
    has_valid_rfd_certificate,
)

from lite_content.lite_exporter_frontend import strings
from lite_content.lite_exporter_frontend.goods import AddGoodToApplicationForm
from lite_forms.helpers import conditional
from lite_forms import components


def exhibition_item_type(request, good_id, application_id):
    return components.Form(
        title=AddGoodToApplicationForm.Exhibition.TITLE,
        description=AddGoodToApplicationForm.Exhibition.DESCRIPTION,
        questions=[
            components.HiddenField(name="good_id", value=good_id),
            components.RadioButtons(title="", description="", name="item_type", options=get_item_types(request)),
        ],
        back_link=components.BackLink(
            AddGoodToApplicationForm.Exhibition.BACK_LINK,
            reverse_lazy("applications:preexisting_good", kwargs={"pk": application_id}),
        ),
    )


def good_on_application_form_group(
    request,
    is_preexisting,
    good,
    sub_case_type,
    draft_pk,
    application,
    show_attach_rfd,
    relevant_firearm_act_section,
    back_url,
    show_serial_numbers_form,
    is_rfd,
):
    # is_preexisting are only asked if user is adding a preexisting good from their product list
    # but not if the good being added to the application is a new good created as part of this same flow
    firearm_type = None
    number_of_items = None
    if good.get("firearm_details"):
        firearm_type = good["firearm_details"]["type"]["key"]
        if "number_of_items" in good["firearm_details"]:
            number_of_items = good["firearm_details"]["number_of_items"]

    is_firearm_core = firearm_type and firearm_type in FIREARM_AMMUNITION_COMPONENT_TYPES
    show_rfd_question = is_firearm_core and not has_valid_rfd_certificate(application)

    show_firearm_act_confirmation = is_preexisting and is_firearm_core
    return components.FormGroup(
        [
            conditional(is_preexisting and is_firearm_core, firearms_number_of_items(firearm_type)),
            conditional(is_preexisting and is_firearm_core, identification_markings_form(draft_pk)),
            conditional(
                is_preexisting and is_firearm_core and show_serial_numbers_form,
                firearms_capture_serial_numbers(number_of_items),
            ),
            conditional(is_preexisting, firearm_year_of_manufacture_details_form()),
            unit_quantity_value(
                request=request, good=good, sub_case_type=sub_case_type, application_id=draft_pk, back_url=back_url
            ),
            conditional(is_preexisting and show_rfd_question, is_registered_firearm_dealer_field(back_url)),
            conditional(is_preexisting and show_attach_rfd, attach_firearm_dealer_certificate_form(back_url)),
            conditional(show_firearm_act_confirmation, firearms_act_confirmation_form(is_rfd)),
        ]
    )


def unit_quantity_value(request, good, sub_case_type, application_id, back_url):
    if sub_case_type["key"] == EXHIBITION:
        return exhibition_item_type(request, good.get("id"), application_id)
    else:
        initial_questions = [
            good_summary(good),
            components.HiddenField(name="good_id", value=good.get("id")),
            components.Select(
                title=AddGoodToApplicationForm.Units.TITLE,
                description="<noscript>" + AddGoodToApplicationForm.Units.DESCRIPTION + "</noscript>",
                name="unit",
                options=get_units(request),
            ),
            components.QuantityInput(
                title=AddGoodToApplicationForm.Quantity.TITLE,
                description=AddGoodToApplicationForm.Quantity.DESCRIPTION,
                name="quantity",
            ),
            components.CurrencyInput(
                title=AddGoodToApplicationForm.VALUE.TITLE,
                description=AddGoodToApplicationForm.VALUE.DESCRIPTION,
                name="value",
            ),
            components.RadioButtons(
                name="is_good_incorporated",
                title=AddGoodToApplicationForm.Incorporated.TITLE,
                description=AddGoodToApplicationForm.Incorporated.DESCRIPTION,
                options=[
                    components.Option(True, AddGoodToApplicationForm.Incorporated.YES),
                    components.Option(False, AddGoodToApplicationForm.Incorporated.NO),
                ],
                classes=["govuk-radios--inline"],
            ),
        ]

        questions = []
        if good["item_category"]["key"] == PRODUCT_CATEGORY_FIREARM:
            firearm_type = good["firearm_details"]["type"]["key"]

            # for these types we capture quantity as number of items and
            # units default to number of articles
            if firearm_type in FIREARM_AMMUNITION_COMPONENT_TYPES:
                for question in initial_questions:
                    if hasattr(question, "name") and question.name in ["quantity", "unit"]:
                        continue
                    questions.append(question)
            else:
                questions = initial_questions

            if firearm_type in ["ammunition", "firearms"]:
                questions.append(firearm_proof_mark_field())
            elif firearm_type == "components_for_firearms":
                questions.append(does_firearm_component_require_proof_marks_field())
            questions.append(firearm_is_deactivated_field())
        else:
            questions = initial_questions

        return components.Form(
            title=AddGoodToApplicationForm.TITLE,
            description=AddGoodToApplicationForm.DESCRIPTION,
            questions=questions,
            back_link=components.BackLink(strings.BACK_TO_APPLICATION, back_url),
            javascript_imports={"/javascripts/add-good.js"},
        )


def does_firearm_component_require_proof_marks_field():
    return components.RadioButtons(
        title="Is the product a gun barrel or the action of a gun?",
        name="is_gun_barrel",
        options=[
            components.Option(key=True, value="Yes", components=[firearm_proof_mark_field()],),
            components.Option(key=False, value="No"),
        ],
    )


def firearm_proof_mark_field():
    return components.RadioButtons(
        title="Does the product have valid UK proof marks?",
        name="has_proof_mark",
        options=[
            components.Option(key=True, value="Yes"),
            components.Option(
                key=False,
                value="No",
                components=[
                    components.TextArea(
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
    return components.RadioButtons(
        title="Has the product been deactivated?",
        name="is_deactivated",
        options=[
            components.Option(
                key=True,
                value="Yes",
                components=[
                    components.DateInput(
                        title="Date of deactivation", name="date_of_deactivation", prefix="date_of_deactivation",
                    ),
                    components.RadioButtons(
                        title="Has the product been deactivated to UK/EU proof house standards?",
                        name="is_deactivated_to_standard",
                        options=[
                            components.Option(
                                key=True,
                                value="Yes",
                                components=[
                                    components.Select(
                                        title="Proof house standard",
                                        name="deactivation_standard",
                                        options=[
                                            components.Option(key="UK", value="UK"),
                                            components.Option(key="EU", value="EU"),
                                        ],
                                    ),
                                ],
                            ),
                            components.Option(
                                key=False,
                                value="No",
                                components=[
                                    components.TextArea(
                                        title="Describe who deactivated the product and to what standard it was done",
                                        description="",
                                        name="deactivation_standard_other",
                                        optional=False,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            components.Option(key=False, value="No"),
        ],
    )
