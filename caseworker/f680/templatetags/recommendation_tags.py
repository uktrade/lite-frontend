from collections import defaultdict
from django import template


register = template.Library()


@register.inclusion_tag("f680/case/recommendation/all-teams-recommendations.html", takes_context=True)
def all_teams_recommendation(context):
    teams_recommendations = defaultdict(list)
    if context and context.get("case", {}).get("advice"):
        case = context.get("case")

        for item in case["advice"]:
            teams_recommendations[item["team"]["name"]].append(item)

    all_teams_recommendations = []
    for item in sorted(teams_recommendations.keys()):
        # There is going to be only one object for F680 but we get a list
        # from serializer
        recommendations = teams_recommendations.get(item, [])
        decision_string = ""
        decisions = {r["type"]["key"] for r in recommendations}
        if decisions == {"approve"}:
            decision_string = "has approved"
        elif decisions == {"proviso"}:
            decision_string = "has approved with licence conditions"

        all_teams_recommendations.append(
            {"team": item, "recommendations": teams_recommendations.get(item, []), "decision": decision_string}
        )
    context["teams_recommendations"] = all_teams_recommendations

    return context
