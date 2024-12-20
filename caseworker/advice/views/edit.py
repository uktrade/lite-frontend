from caseworker.advice.forms.approval import (
    FootnotesApprovalAdviceForm,
    RecommendAnApprovalForm,
    SimpleLicenceConditionsForm,
)
from caseworker.advice.views.approval import BaseApprovalAdviceView
from caseworker.advice import services
from caseworker.advice.constants import AdviceSteps
from caseworker.advice.picklist_helpers import approval_picklist, footnote_picklist


class EditAdviceView(BaseApprovalAdviceView):

    form_list = [
        (AdviceSteps.RECOMMEND_APPROVAL, RecommendAnApprovalForm),
        (AdviceSteps.LICENCE_CONDITIONS, SimpleLicenceConditionsForm),
        (AdviceSteps.LICENCE_FOOTNOTES, FootnotesApprovalAdviceForm),
    ]

    step_kwargs = {
        AdviceSteps.RECOMMEND_APPROVAL: approval_picklist,
        AdviceSteps.LICENCE_CONDITIONS: None,
        AdviceSteps.LICENCE_FOOTNOTES: footnote_picklist,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_link_url"] = self.get_success_url()
        return context

    def get_form_initial(self, step):
        my_advice = services.filter_current_user_advice(self.case.advice, self.caseworker_id)
        advice = my_advice[0]

        # When the form is prepopulated in the edit flow,
        # the radio values are set to other because only the textfield values are stored it's not possible to replay the selected radio.
        return {
            "add_licence_conditions": bool(advice.get("proviso")),
            "approval_reasons": advice.get("text", ""),
            "approval_radios": "other",
            "proviso": advice.get("proviso"),
            "instructions_to_exporter": advice.get("note", ""),
            "footnote_details": advice.get("footnote", ""),
            "footnote_details_radios": "other",
        }
