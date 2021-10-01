from django.urls import path

from caseworker.advice.views import advicePlaceholderView

urlpatterns = [
    path("", advicePlaceholderView.as_view(), name="advice_placeholder"),
]
