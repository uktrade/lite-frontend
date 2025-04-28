from collections import defaultdict

from core import client


def filter_current_user_recommendation(all_recommendation, user_id):
    return [recommendation for recommendation in all_recommendation if (recommendation["user"]["id"] == user_id)]


def filter_recommendation_by_team(all_recommendation, team_id):
    return [recommendation for recommendation in all_recommendation if recommendation["team"]["id"] == team_id]


def group_recommendations_by_user(recommendation):
    result = defaultdict(list)
    for item in recommendation:
        result[item["user"]["id"]].append(item)
    return result


def group_recommendations_by_team_and_users(case_recommendations):
    """
    Groups all recommendations on a case by team and users.
    Within each team the recommendations are grouped by users.
    """
    grouped_data = defaultdict(lambda: defaultdict(list))

    for recommendation in case_recommendations:
        team_id = recommendation["team"]["id"]
        user_id = recommendation["user"]["id"]
        grouped_data[team_id][user_id].append(recommendation)

    grouped_result = []
    for team_id, user_recommendations_dict in grouped_data.items():
        team = next(item["team"] for item in case_recommendations if item["team"]["id"] == team_id)
        users = [
            {
                "user": next(r["user"] for r in user_recommendations_dict[user_id]),
                "recommendations": user_recommendations_dict[user_id],
            }
            for user_id in user_recommendations_dict
        ]
        grouped_result.append(
            {
                "team": team,
                "users": users,
            }
        )

    return grouped_result


def recommendations_by_current_user(request, case, caseworker):
    team_id = caseworker["team"]["id"]
    caseworker_id = caseworker["id"]

    case_recommendations = get_case_recommendations(request, case)
    recommendation = filter_current_user_recommendation(case_recommendations, caseworker_id)
    recommendation = filter_recommendation_by_team(recommendation, team_id)
    grouped_recommendation = group_recommendations_by_user(recommendation)
    return grouped_recommendation.get(caseworker_id, [])


def get_pending_recommendation_requests(request, case, caseworker):
    recommendations = recommendations_by_current_user(request, case, caseworker)
    completed_release_requests = [item["security_release_request"]["id"] for item in recommendations]
    return {
        rr["id"]: rr for rr in case["data"]["security_release_requests"] if rr["id"] not in completed_release_requests
    }


def get_case_recommendations(request, case):
    response = client.get(request, f"/caseworker/f680/{case['id']}/recommendation/")
    response.raise_for_status()

    recommendations = response.json()
    for item in recommendations:
        release_id = item["security_release_request"]
        item["security_release_request"] = next(
            item for item in case["data"]["security_release_requests"] if item["id"] == release_id
        )

    return recommendations


def post_recommendation(request, case, data):
    json = [
        {
            "type": data["recommendation"],
            "security_grading": data.get("security_grading", ""),
            "security_grading_other": data.get("security_grading_other", ""),
            "conditions": data.get("conditions", ""),
            "refusal_reasons": data.get("refusal_reasons", ""),
            "security_release_request": release_request_id,
        }
        for release_request_id in data["release_requests"]
    ]
    response = client.post(request, f"/caseworker/f680/{case['id']}/recommendation/", json)
    return response.json(), response.status_code


def clear_recommendation(request, case):
    response = client.delete(request, f"/caseworker/f680/{case['id']}/recommendation/")
    return None, response.status_code
