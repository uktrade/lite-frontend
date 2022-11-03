from .constants import AddGoodComponentSteps


def is_component(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(AddGoodComponentSteps.IS_COMPONENT)
    return cleaned_data.get("is_component")
