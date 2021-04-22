from django.urls import path

from core.feedback.views import FeedbackView, get_thanks

urlpatterns = [
    path("", FeedbackView.as_view(), name="feedback"),
    path("/thanks/", get_thanks, name="thanks"),
]
