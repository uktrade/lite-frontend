from .constants import AddUserSteps
from exporter.core.constants import Roles


def is_agent_role(wizard):
    role_select = wizard.get_cleaned_data_for_step(AddUserSteps.SELECT_ROLE)
    return role_select.get("role") == Roles.AGENT_USER_ROLE[0]
