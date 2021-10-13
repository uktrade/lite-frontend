from django.views.generic import FormView, TemplateView

from caseworker.advice import forms, services
from caseworker.cases.services import get_case
from core.auth.views import LoginRequiredMixin
from django.views.generic import TemplateView, FormView


class CaseContextMixin(LoginRequiredMixin):
    """Most advice views need a reference to the associated
    Case object. This mixin, injects a reference to the Case
    in the context.
    """

    def get_context(self):
        return {}

    def get_context_data(self, *args, **kwargs):
        context = super(CaseContextMixin, self).get_context_data(**kwargs)
        case_id = str(self.kwargs["pk"])
        # Ideally, we would probably want to not use the following
        # That said, if you look at the code, it is functional and
        # doesn't have anything to do with e.g. lite-forms
        # P.S. the case here is needed for rendering the base
        # template (layouts/case.html) from which we are inheriting.
        case = get_case(self.request, case_id)
        return {**context, **self.get_context(), "case": case}


class AdvicePlaceholderView(CaseContextMixin, TemplateView):
    """This is POC ATM and should be removed with the first PR
    of advice. Currently, this is a TemplateView but it should
    be fairly simple to make this e.g. a SingleFormView.
    """

    template_name = "advice/placeholder.html"

    def get_context(self):
        return {"greetings": "Hello World!"}


class CaseDetailView(CaseContextMixin, TemplateView):
    """This endpoint renders case detail panel. This will probably
    not be used stand-alone. This is useful for testing the case
    detail template ATM.
    """

    template_name = "advice/case_detail_example.html"


class SelectAdviceView(CaseContextMixin, FormView):
    template_name = "advice/select_advice.html"
    form_class = forms.SelectAdviceForm

    def get_success_url(self):
        recommendation = self.request.POST.get("recommendation")
        if recommendation == "approve_all":
            return "/#approve"
        else:
            return "/#refuse"


class GiveApprovalAdviceView(CaseContextMixin, FormView):
    """
    Form to recommend approval advice for all products on the application
    """

    form_class = forms.GiveApprovalAdviceForm
    template_name = "advice/give-approval-advice.html"

    def get(self, request, *args, **kwargs):
        """
        FormView doesn't pass kwargs to get_context_data() by default in get()
        so override and send kwargs
        """
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_form_kwargs(self):
        # default method supplies different set of kwargs so override and append ours
        default_kwargs = super().get_form_kwargs()
        return {**self.kwargs, **default_kwargs}

    def form_valid(self, form):
        case = self.get_context_data()["case"]
        services.post_advice(self.request, case, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return "/#save-advice"
