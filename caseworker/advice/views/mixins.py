from django.utils.functional import cached_property

from caseworker.advice import services
from caseworker.cases.services import get_case
from caseworker.core.services import get_denial_reasons
from caseworker.users.services import get_gov_user

from core.constants import SecurityClassifiedApprovalsType


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

    @cached_property
    def denial_reasons_display(self):
        denial_reasons_data = get_denial_reasons(self.request)
        return {denial_reason["id"]: denial_reason["display_value"] for denial_reason in denial_reasons_data}

    @property
    def security_approvals_classified_display(self):
        security_approvals = self.case["data"].get("security_approvals")
        if security_approvals:
            security_approvals_dict = dict(SecurityClassifiedApprovalsType.choices)
            return ", ".join([security_approvals_dict[approval] for approval in security_approvals])
        return ""

    @property
    def caseworker_id(self):
        return str(self.request.session["lite_api_user_id"])

    @property
    def caseworker(self):
        data, _ = get_gov_user(self.request, self.caseworker_id)
        return data["user"]

    @property
    def goods(self):
        for index, good_on_application in enumerate(self.case["data"].get("goods", []), start=1):
            good_on_application["line_number"] = index

        return self.case["data"].get("goods", [])

    def get_context(self, **kwargs):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ideally, we would probably want to not use the following
        # That said, if you look at the code, it is functional and
        # doesn't have anything to do with e.g. lite-forms
        # P.S. the case here is needed for rendering the base
        # template (layouts/case.html) from which we are inheriting.

        is_in_lu_team = self.caseworker["team"]["alias"] == services.LICENSING_UNIT_TEAM
        rejected_lu_countersignature = None
        if is_in_lu_team:
            rejected_lu_countersignature = self.rejected_countersign_advice()

        return {
            **context,
            **self.get_context(case=self.case),
            "case": self.case,
            "queue_pk": self.kwargs["queue_pk"],
            "caseworker": self.caseworker,
            "is_lu_countersigning": is_in_lu_team,
            "rejected_lu_countersignature": rejected_lu_countersignature,
        }

    def rejected_countersign_advice(self):
        """
        Return rejected countersignature. Due to the routing, there should only ever be one
        rejection (case will be returned to edit the advice once a rejection has occurred.
        """
        for cs in self.case.get("countersign_advice", []):
            if cs["valid"] and not cs["outcome_accepted"]:
                return cs
        return None


class DESNZNuclearMixin:
    def is_trigger_list_assessed(self, product):
        """Returns True if a product has been assessed for trigger list criteria"""
        return product.get("is_trigger_list_guidelines_applicable") in [True, False]

    @property
    def unassessed_trigger_list_goods(self):
        return [
            product
            for product in services.filter_trigger_list_products(self.goods)
            if not self.is_trigger_list_assessed(product)
        ]

    @property
    def assessed_trigger_list_goods(self):
        return [
            product
            for product in services.filter_trigger_list_products(self.goods)
            if self.is_trigger_list_assessed(product)
        ]
