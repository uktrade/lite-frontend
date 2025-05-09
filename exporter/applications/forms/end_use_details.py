from lite_content.lite_exporter_frontend import (
    generic,
    strings,
)
from lite_content.lite_exporter_frontend.applications import (
    EndUseDetails,
    StandardApplicationTaskList,
)
from lite_forms.components import (
    BackLink,
    Form,
    FormGroup,
    Option,
    RadioButtons,
    TextArea,
    TextInput,
)
from lite_forms.helpers import conditional


def end_use_details_form(application, request, back_link):
    is_eu_military = request.POST.get("is_eu_military", "").lower() == "true" or application.is_eu_military
    caption = StandardApplicationTaskList.END_USE_DETAILS

    return FormGroup(
        [
            intended_end_use_form(caption=caption, back_link=back_link),
            is_military_end_use_controls_form(caption),
            is_informed_wmd_form(caption),
            is_suspected_wmd_form(caption),
            is_eu_military_form(caption),
            conditional(is_eu_military, is_compliant_limitations_eu_form(caption)),
        ]
    )


def intended_end_use_form(caption, back_link):
    return Form(
        caption=caption,
        back_link=BackLink(strings.BACK_TO_APPLICATION, back_link),
        title=EndUseDetails.INTENDED_END_USE,
        questions=[
            TextArea(
                name="intended_end_use",
                short_title=EndUseDetails.EndUseDetailsSummaryList.INTENDED_END_USE,
                extras={"max_length": 2200},
                optional=False,
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def is_military_end_use_controls_form(caption):
    return Form(
        caption=caption,
        title=EndUseDetails.INFORMED_TO_APPLY,
        questions=[
            RadioButtons(
                name="is_military_end_use_controls",
                short_title=EndUseDetails.EndUseDetailsSummaryList.INFORMED_TO_APPLY,
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextInput(
                                title=EndUseDetails.REFERENCE,
                                description=EndUseDetails.REFERENCE_ECJU_LETTER,
                                name="military_end_use_controls_ref",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def is_informed_wmd_form(caption):
    return Form(
        caption=caption,
        title=EndUseDetails.INFORMED_WMD,
        questions=[
            RadioButtons(
                name="is_informed_wmd",
                short_title=EndUseDetails.EndUseDetailsSummaryList.INFORMED_WMD,
                title="",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextInput(
                                title=EndUseDetails.REFERENCE,
                                description=EndUseDetails.REFERENCE_ECJU_LETTER,
                                name="informed_wmd_ref",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def is_suspected_wmd_form(caption):
    return Form(
        caption=caption,
        title=EndUseDetails.SUSPECTED_WMD,
        questions=[
            RadioButtons(
                name="is_suspected_wmd",
                short_title=EndUseDetails.EndUseDetailsSummaryList.SUSPECTED_WMD,
                title="",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                name="suspected_wmd_ref",
                                title="",
                                description=EndUseDetails.PROVIDE_DETAILS,
                                extras={"max_length": 2200},
                                optional=False,
                            )
                        ],
                    ),
                    Option(key=False, value="No"),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def is_eu_military_form(caption):
    return Form(
        caption=caption,
        title=EndUseDetails.EU_MILITARY,
        questions=[
            RadioButtons(
                name="is_eu_military",
                short_title=EndUseDetails.EndUseDetailsSummaryList.EU_MILITARY,
                options=[Option(key=True, value="Yes"), Option(key=False, value="No")],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


def is_compliant_limitations_eu_form(caption):
    return Form(
        caption=caption,
        title=EndUseDetails.IS_COMPLIANT_LIMITATIONS_EU,
        questions=[
            RadioButtons(
                name="is_compliant_limitations_eu",
                short_title=EndUseDetails.EndUseDetailsSummaryList.COMPLIANT_LIMITATIONS_EU,
                options=[
                    Option(key=True, value="Yes"),
                    Option(
                        key=False,
                        value="No",
                        components=[
                            TextArea(
                                name="compliant_limitations_eu_ref",
                                title="",
                                description=EndUseDetails.PROVIDE_DETAILS,
                                extras={"max_length": 2200},
                                optional=False,
                            )
                        ],
                    ),
                ],
            )
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )
