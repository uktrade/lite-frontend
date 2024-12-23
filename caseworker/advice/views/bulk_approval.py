from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


from core.auth.views import LoginRequiredMixin


class BulkApprovalView(LoginRequiredMixin, TemplateView):
    """
    Submit approval recommendation for the selected cases
    """

    template_name = "core/form.html"

    def post(self, request, *args, **kwargs):
        return redirect(reverse("queues:cases", kwargs={"queue_pk": self.kwargs["pk"]}))
