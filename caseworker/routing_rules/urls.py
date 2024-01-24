from django.urls import path

from caseworker.routing_rules import views

app_name = "routing_rules"

urlpatterns = [
    path("", views.RoutingRulesList.as_view(), name="list"),
]
