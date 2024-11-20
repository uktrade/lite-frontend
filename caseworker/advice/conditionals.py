from caseworker.advice import services


def form_add_licence_conditions(step_name):
    def _get_form_field_boolean(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step(step_name)
        return cleaned_data.get("add_licence_conditions")

    return _get_form_field_boolean


def DESNZ_team(wizard):
    return wizard.caseworker["team"]["alias"] in services.DESNZ_TEAMS
