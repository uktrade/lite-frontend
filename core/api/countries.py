from django.http import JsonResponse
from rest_framework.views import APIView

from caseworker.core.services import get_countries


class CountriesList(APIView):
    def get(self, request):
        countries = get_countries(request, convert_to_options=False)
        return JsonResponse(data=countries[0])
