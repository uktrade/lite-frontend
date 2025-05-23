from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Fieldset, Layout, Size, Submit, HTML
from django.urls import reverse_lazy
from django import forms

from core.forms.layouts import StarRadioSelect


class HCSATminiform(forms.Form):
    class Layout:
        TITLE = ""

    RECOMMENDATION_CHOICES = [
        ("VERY_DISSATISFIED", "Very dissatisfied"),
        ("DISSATISFIED", "Dissatisfied"),
        ("NEITHER", "Neutral"),
        ("SATISFIED", "Satisfied"),
        ("VERY_SATISFIED", "Very satisfied"),
    ]

    satisfaction_rating = forms.ChoiceField(
        choices=RECOMMENDATION_CHOICES,
        widget=forms.RadioSelect,
        help_text="",
        label="",
        error_messages={"required": "Star rating is required"},
    )

    def get_title(self):
        return self.title

    def __init__(self, service_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = f"Overall, how would you rate your experience with the '{service_name}' service today?"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                StarRadioSelect("satisfaction_rating"),
                legend=self.get_title(),
                legend_size=Size.MEDIUM,
                legend_tag="h2",
            ),
            Submit("submit", "Submit and continue"),
        )


class HCSATApplicationForm(HCSATminiform):

    EXPERIENCED_ISSUE = [
        ("NO_ISSUE", "I did not experience any issue"),
        ("NOT_FIND_LOOKING_FOR", "The process of submitting my application form was unclear"),
        ("DIFFICULT_TO_NAVIGATE", "I found it difficult to navigate the service"),
        ("SYSTEM_LACKS_FEATURE", "The service lacks a feature I need"),
        ("SYSTEM_SLOW", "The service was slow"),
        ("OTHER", "Other"),
    ]

    other_detail = forms.CharField(
        label="Please describe the issue you experienced",
        widget=forms.Textarea,
        required=False,
        max_length=1200,
    )

    experienced_issues = forms.MultipleChoiceField(
        choices=EXPERIENCED_ISSUE,
        widget=forms.CheckboxSelectMultiple,
        label="Did you experience any of the following issues?",
        help_text="Tick all that apply",
        required=False,
    )

    HELPFUL_GUIDANCE = [
        ("STRONGLY_DISAGREE", "Strongly disagree"),
        ("DISAGREE", "Disagree"),
        ("NEITHER", "Neither agree nor disagree"),
        ("AGREE", "Agree"),
        ("STRONGLY_AGREE", "Strongly agree"),
    ]
    guidance_application_process_helpful = forms.ChoiceField(
        choices=HELPFUL_GUIDANCE,
        widget=forms.RadioSelect,
        label="To what extent do you agree that the guidance available during the application process was helpful?",
        required=False,
    )

    USER_ACCOUNT_PROCESS = [
        ("ALREADY_HAD_ACCOUNT", "I already had an account"),
        ("VERY_DIFFICULT", "Very difficult"),
        ("DIFFICULT", "Difficult"),
        ("NEITHER", "Neither easy nor difficult"),
        ("EASY", "Easy"),
        ("VERY_EASY", "Very easy"),
    ]
    process_of_creating_account = forms.ChoiceField(
        choices=USER_ACCOUNT_PROCESS,
        widget=forms.RadioSelect,
        label="How would you describe the process of creating a user account on this service?",
        required=False,
    )

    service_improvements_feedback = forms.CharField(
        label="How could we improve this service?",
        widget=forms.Textarea,
        help_text="Do not include any personal information, like your name or email address",
        required=False,
        max_length=1200,
    )

    def __init__(self, service_name, *args, **kwargs):
        super().__init__(service_name, *args, **kwargs)
        legend_size = "m"
        help_text = f"Overall, how would you rate your experience with the '{service_name}' service today?"
        self.fields["satisfaction_rating"].help_text = help_text

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("satisfaction_rating", type="hidden"),
            Field.radios("experienced_issues", legend_size=legend_size, legend_tag="h1"),
            Field.textarea("other_detail", max_characters=1200, aria_describedby="other_detail"),
            Field.radios("guidance_application_process_helpful", legend_size=legend_size, legend_tag="h1"),
            Field.radios("process_of_creating_account", legend_size=legend_size, legend_tag="h1"),
            Field.textarea(
                "service_improvements_feedback",
                max_characters=1200,
                aria_describedby="service_improvements_feedback",
                label_size="m",
            ),
            Submit("submit", "Submit feedback"),
            HTML(f'<a href="{reverse_lazy("core:home")}" class="govuk-button govuk-button--secondary">Cancel</a>'),
        )
