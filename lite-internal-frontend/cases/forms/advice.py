from cases.constants import CaseType
from lite_forms.components import Form, RadioButtons, Option, BackLink
from lite_content.lite_internal_frontend.strings import cases


def advice_recommendation_form(post_url, back_url, application_type):
    if application_type == CaseType.OPEN_LICENCE.value:
        denial_option = Option("refuse", cases.AdviceRecommendationForm.RadioButtons.REJECT)
    else:
        denial_option = Option("refuse", cases.AdviceRecommendationForm.RadioButtons.REFUSE)

    return Form(
        cases.AdviceRecommendationForm.TITLE,
        cases.AdviceRecommendationForm.DESCRIPTION,
        [
            RadioButtons(
                "type",
                [
                    Option("approve", cases.AdviceRecommendationForm.RadioButtons.GRANT),
                    Option("proviso", cases.AdviceRecommendationForm.RadioButtons.PROVISO),
                    denial_option,
                    Option("no_licence_required", cases.AdviceRecommendationForm.RadioButtons.NLR),
                    Option("not_applicable", cases.AdviceRecommendationForm.RadioButtons.NOT_APPLICABLE, show_or=True),
                ],
            ),
        ],
        default_button_name=cases.AdviceRecommendationForm.Actions.CONTINUE_BUTTON,
        back_link=BackLink(cases.AdviceRecommendationForm.Actions.BACK_BUTTON, back_url),
        post_url=post_url,
    )
