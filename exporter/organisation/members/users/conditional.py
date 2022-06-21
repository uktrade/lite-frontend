from .constants import AddUserSteps
from exporter.core.enums import Roles


def is_agent_role(wizard):
    role_select = wizard.get_cleaned_data_for_step(AddUserSteps.SELECT_ROLE)
    return role_select.get("role") == Roles.agent.id
