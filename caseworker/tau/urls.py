from django.urls import path

from caseworker.tau.views import TAUHome, TAUEdit

app_name = "tau"

urlpatterns = [
    path("", TAUHome.as_view(), name="home"),
    path("edit/<good_id>", TAUEdit.as_view(), name="edit"),
]
