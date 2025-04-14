from caseworker.f680.recommendation.constants import RecommendationSteps, RecommendationType


def is_approving(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(RecommendationSteps.ENTITIES_AND_DECISION)
    return cleaned_data.get("recommendation") == RecommendationType.APPROVE


def is_refusing(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(RecommendationSteps.ENTITIES_AND_DECISION)
    return cleaned_data.get("recommendation") == RecommendationType.REFUSE


def team_provisos_exist(wizard):
    return len(wizard.conditions["results"]) > 0


def denial_reasons_exist(wizard):
    return len(wizard.refusal_reasons) > 0
