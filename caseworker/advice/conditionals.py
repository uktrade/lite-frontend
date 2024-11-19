from caseworker.advice import services


def add_conditions(step_name):
    def _get_form_field_boolean(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step(step_name)
        return cleaned_data.get("add_conditions")

    return _get_form_field_boolean


def FCDO_team(wizard):
    return wizard.caseworker["team"]["alias"] == services.FCDO_TEAM


def DESNZ_team(wizard):
    return wizard.caseworker["team"]["alias"] in services.DESNZ_TEAMS
