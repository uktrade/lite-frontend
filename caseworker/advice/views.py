from django.views.generic import FormView, TemplateView
from django.urls import reverse

from caseworker.advice import forms, services
from caseworker.cases.services import get_case
from caseworker.core.services import get_denial_reasons
from core.auth.views import LoginRequiredMixin


class CaseContextMixin:
    """Most advice views need a reference to the associated
    Case object. This mixin, injects a reference to the Case
    in the context.
    """

    def get_context(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super(CaseContextMixin, self).get_context_data(**kwargs)
        case_id = str(self.kwargs["pk"])
        # Ideally, we would probably want to not use the following
        # That said, if you look at the code, it is functional and
        # doesn't have anything to do with e.g. lite-forms
        # P.S. the case here is needed for rendering the base
        # template (layouts/case.html) from which we are inheriting.
        case = get_case(self.request, case_id)
        return {**context, **self.get_context(), "case": case, "queue_pk": self.kwargs["queue_pk"]}


class AdvicePlaceholderView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    """This is POC ATM and should be removed with the first PR
    of advice. Currently, this is a TemplateView but it should
    be fairly simple to make this e.g. a SingleFormView.
    """

    template_name = "advice/placeholder.html"

    def get_context(self):
        return {"greetings": "Hello World!"}


class CaseDetailView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    """This endpoint renders case detail panel. This will probably
    not be used stand-alone. This is useful for testing the case
    detail template ATM.
    """

    template_name = "advice/case_detail_example.html"


class SelectAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/select_advice.html"
    form_class = forms.SelectAdviceForm

    def get_success_url(self):
        recommendation = self.request.POST.get("recommendation")
        if recommendation == "approve_all":
            return reverse("cases:approve_all", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})
        else:
            return "/#refuse"


class GiveApprovalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    """
    Form to recommend approval advice for all products on the application
    """

    form_class = forms.GiveApprovalAdviceForm
    template_name = "advice/give-approval-advice.html"
    success_url = "/#save-advice"

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.post_approval_advice(self.request, case, form.cleaned_data)
        return super().form_valid(form)


class RefusalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/refusal_advice.html"
    form_class = forms.RefusalAdviceForm
    success_url = "/#save-advice"

    def get_form_kwargs(self):
        """Overriding this so that I can pass denial_reasons
        to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs["denial_reasons"] = get_denial_reasons(self.request)
        return kwargs

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.post_refusal_advice(self.request, case, form.cleaned_data)
        return super().form_valid(form)


class AdviceDetailView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    template_name = "advice/view_my_advice.html"

    def current_user_advice(self, case):
        return [
            advice
            for advice in case.advice
            if advice["type"]["key"] in ["approve", "proviso", "refuse"]
            and (advice["user"]["id"] == str(self.request.session["lite_api_user_id"]))
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_advice = self.current_user_advice(context["case"])
        nlr_products = services.filter_nlr_products(context["case"]["data"]["goods"])
        return {**context, "my_advice": my_advice, "nlr_products": nlr_products}


class DeleteAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/delete-advice.html"
    form_class = forms.DeleteAdviceForm

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.delete_user_advice(self.request, case["id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={"queue_pk": self.kwargs["queue_pk"], "pk": self.kwargs["pk"]})
