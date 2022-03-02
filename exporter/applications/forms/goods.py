from django.urls import reverse_lazy

from exporter.core.services import get_units, get_item_types

from lite_content.lite_exporter_frontend.goods import AddGoodToApplicationForm
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


def get_units_options(request):
    parsed = get_units(request)
    units = []
    for key, value in parsed.items():
        units.append(components.Option(key, value))
    return units


def does_firearm_component_require_proof_marks_field():
    return components.RadioButtons(
        title="Is the product a gun barrel or the action of a gun?",
        name="is_gun_barrel",
        options=[
            components.Option(
                key=True,
                value="Yes",
                components=[firearm_proof_mark_field()],
            ),
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
                        title="Date of deactivation",
                        name="date_of_deactivation",
                        prefix="date_of_deactivation",
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
