from exporter.goods.forms.firearms import FirearmSection5Form


def get_is_covered_by_section_5_initial_data(firearm_details):
    is_covered_by_firearm_act_section_one_two_or_five = firearm_details.get(
        "is_covered_by_firearm_act_section_one_two_or_five"
    )

    if is_covered_by_firearm_act_section_one_two_or_five is None:
        return {}

    if (
        is_covered_by_firearm_act_section_one_two_or_five == "Yes"
        and firearm_details["firearms_act_section"] == "firearms_act_section5"
    ):
        return {"is_covered_by_section_5": FirearmSection5Form.Section5Choices.YES}

    if is_covered_by_firearm_act_section_one_two_or_five == "No":
        return {"is_covered_by_section_5": FirearmSection5Form.Section5Choices.NO}

    if is_covered_by_firearm_act_section_one_two_or_five == "Unsure":
        is_covered_by_firearm_act_section_one_two_or_five_explanation = firearm_details[
            "is_covered_by_firearm_act_section_one_two_or_five_explanation"
        ]
        return {
            "is_covered_by_section_5": FirearmSection5Form.Section5Choices.DONT_KNOW,
            "not_covered_explanation": is_covered_by_firearm_act_section_one_two_or_five_explanation,
        }
