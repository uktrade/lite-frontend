from django.http import JsonResponse
from rest_framework.views import APIView

from caseworker.regimes.services import get_regime_entries_all


class RegimeEntriesList(APIView):
    def get(self, request):
        regime_entries = get_regime_entries_all(request)
        return JsonResponse(data=regime_entries[0], safe=False)
