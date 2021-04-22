import logging

from django.urls import reverse
from django.shortcuts import render
from django.views.generic import FormView

from core.auth.views import LoginRequiredMixin
from core.feedback.forms import FeedbackForm
from core.feedback.notify import send_feedback, NotifyException


logger = logging.getLogger(__name__)


class FeedbackView(LoginRequiredMixin, FormView):
    template_name = "feedback/form.html"
    form_class = FeedbackForm

    def get_success_url(self):
        return reverse("thanks")

    def form_valid(self, form):
        email = self.request.session["email"]
        try:
            send_feedback(form.cleaned_data["feedback"], email)
        except NotifyException as e:
            # At this point, we have failed to gather feedback.
            # I would think that telling this to the user would
            # not be super useful so we should log the failure
            # and say Thank you!
            logger.error(str(e))
        return super().form_valid(form)


def get_thanks(request):
    return render(request, "feedback/thanks.html")
