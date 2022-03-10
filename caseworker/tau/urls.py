from django.urls import path

from caseworker.tau.views import TAUHome

app_name = "tau"

urlpatterns = [
    path("", TAUHome.as_view(), name="home"),
]
