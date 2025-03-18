from collections import defaultdict

from core import client
from caseworker.f680.recommendation.constants import RecommendationType


def filter_current_user_recommendation(all_recommendation, user_id, levels):
    return [
        recommendation
        for recommendation in all_recommendation
        if recommendation["level"] in levels
        and recommendation["type"]["key"] in ["approve", "proviso", "refuse"]
        and (recommendation["user"]["id"] == user_id)
    ]


def filter_recommendation_by_level(all_recommendation, recommendation_level):
    return [recommendation for recommendation in all_recommendation if recommendation["level"] == recommendation_level]


def filter_recommendation_by_team(all_recommendation, team_id):
    return [recommendation for recommendation in all_recommendation if recommendation["team"]["id"] == team_id]


def group_recommendation_by_user(recommendation):
    result = defaultdict(list)
    for item in recommendation:
        result[item["user"]["id"]].append(item)
    return result


def current_user_recommendation(all_recommendations, caseworker, level):
    team_id = caseworker["team"]["id"]
    caseworker_id = caseworker["id"]

    recommendation = filter_recommendation_by_level(all_recommendations, level)
    recommendation = filter_current_user_recommendation(recommendation, caseworker_id, level)
    recommendation = filter_recommendation_by_team(recommendation, team_id)
    grouped_recommendation = group_recommendation_by_user(recommendation)
    return grouped_recommendation.get(caseworker_id)


def post_recommendation(request, case, data, level="user-advice"):
    json = [
        {
            "type": item["type"],
            "conditions": item["conditions"] if item["type"] == RecommendationType.APPROVE else "",
            "refusal_reasons": item["conditions"] if item["type"] == RecommendationType.REFUSE else "",
            "security_grading": item["security_grading"],
            "security_grading_other": item["security_grading_other"],
            "security_release_request": item["security_release_request"],
        }
        for item in data
    ]
    response = client.post(request, f"/caseworker/f680/{case['id']}/recommendation/", json)
    response.raise_for_status()
    return response.json(), response.status_code
