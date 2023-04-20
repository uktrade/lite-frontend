from django.urls import path

from . import queues, countries, regime_entries

app_name = "api"

urlpatterns = [
    path("teams/<uuid:pk>/queues/", queues.TeamQueuesList.as_view(), name="team-queues"),
    path("countries/", countries.CountriesList.as_view(), name="countries"),
    path("regime-entries/", regime_entries.RegimeEntriesList.as_view(), name="regime-entries"),
]
