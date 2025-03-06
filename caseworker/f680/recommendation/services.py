from collections import defaultdict

from core import client


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
