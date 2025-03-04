from collections import defaultdict

from caseworker.advice import constants
from core import client


def filter_current_user_recommendation(all_recommendation, user_id):
    return [
        recommendation
        for recommendation in all_recommendation
        if recommendation["level"] == constants.AdviceLevel.USER
        and recommendation["type"]["key"] in ["approve", "proviso", "refuse"]
        and (recommendation["user"]["id"] == user_id)
    ]


def filter_recommendation_by_level(all_recommendation, recommendation_levels):
    return [recommendation for recommendation in all_recommendation if recommendation["level"] in recommendation_levels]


def filter_recommendation_by_team(all_recommendation, team_alias):
    return [recommendation for recommendation in all_recommendation if recommendation["team"]["alias"] == team_alias]


def group_recommendation_by_user(recommendation):
    result = defaultdict(list)
    for item in recommendation:
        result[item["user"]["id"]].append(item)
    return result


def get_current_user_recommendation(recommendation, caseworker_id, team_alias):
    user_level_recommendation = filter_recommendation_by_level(recommendation, ["user"])
    user_recommendation = filter_current_user_recommendation(user_level_recommendation, caseworker_id)
    user_recommendation = filter_recommendation_by_team(user_recommendation, team_alias)
    grouped_user_recommendation = group_recommendation_by_user(user_recommendation)
    return grouped_user_recommendation.get(caseworker_id)


def post_approval_recommendation(request, case, data, level="user-advice"):
    json = [
        {
            "type": "proviso" if data.get("proviso", False) else "approve",
            "text": data["approval_reasons"],
            "proviso": data.get("proviso", ""),
            "note": data.get("instructions_to_exporter", ""),
            "footnote_required": True if data.get("footnote_details") else False,
            "footnote": data.get("footnote_details", ""),
            "denial_reasons": [],
        }
    ]
    response = client.post(request, f"/cases/{case['id']}/{level}/", json)
    response.raise_for_status()
    return response.json(), response.status_code
