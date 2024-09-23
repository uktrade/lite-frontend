from .constants import AddUserSteps
from core.constants import ExporterRoles


def is_agent_role(wizard):
    role_select = wizard.get_cleaned_data_for_step(AddUserSteps.SELECT_ROLE)
    return role_select.get("role") == ExporterRoles.agent.id
