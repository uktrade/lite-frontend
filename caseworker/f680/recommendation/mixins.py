from django.utils.functional import cached_property

from caseworker.cases.services import get_case
from caseworker.users.services import get_gov_user


class CaseContextMixin:
    """Most advice views need a reference to the associated
    Case object. This mixin, injects a reference to the Case
    in the context.
    """

    @property
    def case_id(self):
        return str(self.kwargs["pk"])

    @cached_property
    def case(self):
        return get_case(self.request, self.case_id)

    @property
    def caseworker_id(self):
        return str(self.request.session["lite_api_user_id"])

    @property
    def caseworker(self):
        data, _ = get_gov_user(self.request, self.caseworker_id)
        return data["user"]

    def get_context(self, **kwargs):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {
            **context,
            **self.get_context(case=self.case),
            "case": self.case,
            "queue_pk": self.kwargs["queue_pk"],
            "caseworker": self.caseworker,
        }
