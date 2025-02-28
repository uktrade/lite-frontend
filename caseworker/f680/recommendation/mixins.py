
from caseworker.cases.services import get_case
from caseworker.queues.services import get_queue
from caseworker.users.services import get_gov_user


class CaseContextMixin:
    """Most advice views need a reference to the associated
    Case object. This mixin, injects a reference to the Case
    in the context.
    """

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.case_id = str(kwargs["pk"])
        self.case = get_case(request, self.case_id)
        self.queue_id = kwargs["queue_pk"]
        self.queue = get_queue(request, self.queue_id)
        self.caseworker_id = str(self.request.session["lite_api_user_id"])
        data, _ = get_gov_user(self.request, self.caseworker_id)
        self.caseworker = data["user"]

    def get_context(self, **kwargs):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return {
            **context,
            **self.get_context(case=self.case),
            "case": self.case,
            "queue_pk": self.queue_id,
            "caseworker": self.caseworker,
        }
