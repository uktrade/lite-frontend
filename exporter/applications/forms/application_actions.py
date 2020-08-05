from django.urls import reverse_lazy

from applications.helpers.summaries import application_summary
from lite_content.lite_exporter_frontend import strings
from lite_forms.generators import confirm_form


def withdraw_application_confirmation(application, pk):
    return confirm_form(
        title=strings.applications.ApplicationSummaryPage.Withdraw.TITLE,
        confirmation_name="choice",
        summary=application_summary(application),
        back_link_text=strings.applications.ApplicationSummaryPage.Withdraw.BACK_TEXT,
        yes_label=strings.applications.ApplicationSummaryPage.Withdraw.YES_LABEL,
        no_label=strings.applications.ApplicationSummaryPage.Withdraw.NO_LABEL,
        submit_button_text=strings.applications.ApplicationSummaryPage.Withdraw.SUBMIT_BUTTON,
        back_url=reverse_lazy("applications:application", kwargs={"pk": pk}),
        side_by_side=True,
    )


def surrender_application_confirmation(application, pk):
    return confirm_form(
        title=strings.applications.ApplicationSummaryPage.Surrender.TITLE,
        confirmation_name="choice",
        summary=application_summary(application),
        back_link_text=strings.applications.ApplicationSummaryPage.Surrender.BACK_TEXT,
        yes_label=strings.applications.ApplicationSummaryPage.Surrender.YES_LABEL,
        no_label=strings.applications.ApplicationSummaryPage.Surrender.NO_LABEL,
        submit_button_text=strings.applications.ApplicationSummaryPage.Surrender.SUBMIT_BUTTON,
        back_url=reverse_lazy("applications:application", kwargs={"pk": pk}),
        side_by_side=True,
    )
