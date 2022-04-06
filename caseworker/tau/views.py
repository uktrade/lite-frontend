from django.views.generic import FormView
from django.utils.functional import cached_property

from caseworker.cases.services import get_case
from caseworker.tau.forms import TAUAssessmentForm
from core.auth.views import LoginRequiredMixin
from caseworker.core.services import get_control_list_entries
from caseworker.cases.services import post_review_good


class TAUMixin:
    """Mixin containing some useful functions used in TAU views."""

    @cached_property
    def case_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def queue_id(self):
        return str(self.kwargs["queue_pk"])

    @cached_property
    def case(self):
        return get_case(self.request, self.case_id)

    @cached_property
    def control_list_entries(self):
        control_list_entries = get_control_list_entries(self.request, convert_to_options=True)
        return [(item.value, item.key) for item in control_list_entries]

    def is_assessed(self, good):
        """Returns True if a good has been assessed"""
        return (good["is_good_controlled"] is not None) or (good["control_list_entries"] != [])

    @property
    def assessed_goods(self):
        return [item for item in self.case.goods if self.is_assessed(item)]

    @property
    def unassessed_goods(self):
        return [item for item in self.case.goods if not self.is_assessed(item)]

    @property
    def good_id(self):
        return str(self.kwargs["good_id"])


class TAUHome(LoginRequiredMixin, TAUMixin, FormView):
    """This renders a placeholder home page for TAU 2.0."""

    template_name = "tau/home.html"
    form_class = TAUAssessmentForm

    def get_success_url(self):
        return self.request.path

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["control_list_entries_choices"] = self.control_list_entries
        form_kwargs["goods"] = {item["id"]: item for item in self.unassessed_goods}
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            "case": self.case,
            "queue_id": self.queue_id,
            "assessed_goods": self.assessed_goods,
            "unassessed_goods": self.unassessed_goods,
        }

    def get_goods(self, good_ids):
        good_ids_set = set(good_ids)
        for good in self.case.goods:
            if good["id"] in good_ids_set:
                yield good

    def form_valid(self, form):
        data = form.cleaned_data
        # API does not accept `does_not_have_control_list_entries` but it does require `is_good_controlled`.
        # `is_good_controlled`.has an explicit checkbox called "Is a licence required?" in
        # ExportControlCharacteristicsForm. Going forwards, we want to deduce this like so -
        is_good_controlled = not data.pop("does_not_have_control_list_entries")
        good_ids = data.pop("goods")
        for good in self.get_goods(good_ids):
            payload = {
                **form.cleaned_data,
                "current_object": good["id"],
                "objects": [good["good"]["id"]],
                "is_good_controlled": is_good_controlled,
            }
            post_review_good(self.request, case_id=self.kwargs["pk"], data=payload)
        return super().form_valid(form)
