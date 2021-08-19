from rest_framework.views import APIView
from rest_framework.response import Response

from caseworker.teams.services import get_team_queues


class TeamQueuesList(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        teams = get_team_queues(request, pk, convert_to_options=False, ignore_pagination=True)
        return Response(teams)
