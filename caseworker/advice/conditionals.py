from caseworker.advice import services


def form_add_licence_conditions(step_name):
    """Returns the boolean value for add_licence_conditions from the approval form"""

    def _get_form_field_boolean(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step(step_name)
        return cleaned_data.get("add_licence_conditions")

    return _get_form_field_boolean


def is_desnz_team(wizard):
    return wizard.caseworker["team"]["alias"] in services.DESNZ_TEAMS
