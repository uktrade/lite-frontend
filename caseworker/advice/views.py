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

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.post_approval_advice(self.request, case, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})


class RefusalAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    template_name = "advice/refusal_advice.html"
    form_class = forms.RefusalAdviceForm

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

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})


class AdviceDetailView(LoginRequiredMixin, CaseContextMixin, TemplateView):
    template_name = "advice/view_my_advice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case = context["case"]
        my_advice = services.filter_current_user_advice(case.advice, str(self.request.session["lite_api_user_id"]))
        nlr_products = services.filter_nlr_products(case["data"]["goods"])
        return {**context, "my_advice": my_advice, "nlr_products": nlr_products}


class EditAdviceView(LoginRequiredMixin, CaseContextMixin, FormView):
    """
    Form to edit given advice for all products on the application
    """

    def get_form(self):
        case = get_case(self.request, self.kwargs["pk"])
        my_advice = services.filter_current_user_advice(case.advice, str(self.request.session["lite_api_user_id"]))
        if not my_advice:
            raise ValueError("User has not yet given advice for this case")

        advice = my_advice[0]

        if advice["type"]["key"] in ["approve", "proviso"]:
            initial_data = {
                "proviso": advice["proviso"],
                "approval_reasons": advice["text"],
                "instructions_to_exporter": advice["note"],
                "footnote_details": advice["footnote"],
            }
            self.advice_type = "approve"
            self.template_name = "advice/give-approval-advice.html"
            return forms.GiveApprovalAdviceForm(data=initial_data)
        elif advice["type"]["key"] == "refuse":
            initial_data = {
                "refusal_reasons": advice["text"],
                "denial_reasons": [r for r in advice["denial_reasons"]],
            }
            denial_reasons = get_denial_reasons(self.request)

            self.advice_type = "refuse"
            self.template_name = "advice/refusal_advice.html"
            return forms.RefusalAdviceForm(data=initial_data, denial_reasons=denial_reasons)
        else:
            raise ValueError("Invalid advice type encountered")

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        data = form.cleaned_data.copy()
        if form.has_changed():
            if self.advice_type == "approve":
                for field in form.changed_data:
                    data[field] = self.request.POST.get(field)
                services.post_approval_advice(self.request, case, data)
            elif self.advice_type == "refuse":
                data["refusal_reasons"] = self.request.POST.get("refusal_reasons")
                data["denial_reasons"] = self.request.POST.getlist("denial_reasons")
                services.post_refusal_advice(self.request, case, data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("cases:view_my_advice", kwargs={**self.kwargs})
