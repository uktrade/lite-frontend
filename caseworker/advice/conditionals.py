from caseworker.advice import services


def form_add_licence_conditions(step_name):
    """Returns the boolean value for add_licence_conditions from the approval form"""

    def _get_form_field_boolean(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step(step_name)
        return cleaned_data.get("add_licence_conditions", False)

    return _get_form_field_boolean


def is_fcdo_team(wizard):
    return wizard.caseworker["team"]["alias"] == services.FCDO_TEAM


def is_ogd_team(wizard):
    return not is_fcdo_team(wizard)
