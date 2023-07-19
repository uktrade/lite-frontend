from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Fieldset, HTML, Submit, Button, Accordion, AccordionSection

from django import forms
from django.urls import reverse


SLA_DAYS_RANGE = 99


class CasesFiltersForm(forms.Form):
    case_reference = forms.CharField(
        label="Case reference",
        widget=forms.TextInput(attrs={"id": "case_reference"}),
        required=False,
    )
    export_type = forms.ChoiceField(
        label="Permanent or temporary",
        choices=(
            ("", ""),
            ("permanent", "Permanent"),
            ("temporary", "Temporary"),
        ),
        required=False,
    )
    exporter_application_reference = forms.CharField(
        label="Exporter reference",
        required=False,
    )
    organisation_name = forms.CharField(
        label="Organisation name",
        required=False,
    )
    exporter_site_name = forms.CharField(
        label="Site name",
        required=False,
    )
    goods_starting_point = forms.ChoiceField(
        label="Shipping from",
        required=False,
        choices=(("", ""), ("GB", "Great Britain"), ("NI", "Northern Ireland")),
    )
    party_name = forms.CharField(
        label="Party name",
        required=False,
    )
    product_name = forms.CharField(
        label="Product name",
        required=False,
    )
    max_total_value = forms.DecimalField(
        label="Max total value (£)",
        required=False,
        widget=forms.TextInput,
    )
    report_summary = forms.CharField(
        label="Report summary",
        required=False,
    )
    submitted_from = DateInputField(
        label="Submitted after",
        required=False,
    )
    submitted_to = DateInputField(
        label="Submitted before",
        required=False,
    )
    finalised_from = DateInputField(
        label="Finalised after",
        required=False,
    )
    finalised_to = DateInputField(
        label="Finalised before",
        required=False,
    )
    exclude_denial_matches = forms.BooleanField(
        label="Exclude denial matches",
        required=False,
    )
    exclude_sanction_matches = forms.BooleanField(
        label="Exclude sanction matches",
        required=False,
    )
    exclude_control_list_entry = forms.BooleanField(
        label="Exclude control list entries",
        required=False,
    )
    exclude_regime_entry = forms.BooleanField(
        label="Exclude regime entries",
        required=False,
    )
    is_trigger_list = forms.BooleanField(
        label="Trigger list",
        required=False,
    )
    is_nca_applicable = forms.BooleanField(
        label="Nuclear Cooperation Agreement",
        required=False,
    )

    includes_refusal_recommendation_from_ogd = forms.BooleanField(
        label="Includes a refusal recommendation",
        required=False,
    )
    return_to = forms.CharField(
        label="",
        widget=forms.HiddenInput(),
        required=False,
    )

    def get_field_choices(self, filters_data, field):
        return [("", "Select")] + [(choice["key"], choice["value"]) for choice in filters_data.get(field, [])]

    def __init__(self, queue, filters_data, all_flags, all_cles, all_regimes, countries, queues, *args, **kwargs):
        super().__init__(*args, **kwargs)

        case_status_choices = self.get_field_choices(filters_data, "statuses")
        gov_user_choices = [("", "Select"), ("not_assigned", "Not assigned")] + [
            (choice["id"], choice["full_name"]) for choice in filters_data["gov_users"]
        ]

        flags_choices = [(flag["id"], flag["name"]) for flag in all_flags]
        cle_choices = [(cle["rating"], cle["rating"]) for cle in all_cles]
        regime_choices = [(regime["id"], regime["name"]) for regime in all_regimes]
        country_choices = [(country["id"], country["name"]) for country in countries]
        assigned_queues_choices = [(queue["id"], f"{queue['team']['name']}: {queue['name']}") for queue in queues]

        self.fields["status"] = forms.ChoiceField(
            choices=case_status_choices,
            label="Case status",
            required=False,
        )

        self.fields["case_officer"] = forms.ChoiceField(
            choices=gov_user_choices,
            label="Licensing Unit case officer",
            widget=forms.Select(attrs={"id": "case_officer"}),
            required=False,
        )

        self.fields["assigned_user"] = forms.ChoiceField(
            choices=gov_user_choices,
            label="Case adviser",
            widget=forms.Select(attrs={"id": "case_adviser"}),
            required=False,
        )

        flag_url = reverse("flags:flags")
        self.fields["flags"] = forms.MultipleChoiceField(
            label="Flags",
            choices=flags_choices,
            required=False,
            help_text=f'<a href="{flag_url}" class="govuk-link govuk-link--no-visited-state" target="_blank">Flag information (open in a new window)</a>',
            # setting id for javascript to use
            widget=forms.SelectMultiple(attrs={"id": "flags"}),
        )
        self.fields["control_list_entry"] = forms.MultipleChoiceField(
            label="Control list entry",
            choices=cle_choices,
            required=False,
            # setting id for javascript to use
            widget=forms.SelectMultiple(attrs={"id": "control_list_entry"}),
        )
        self.fields["regime_entry"] = forms.MultipleChoiceField(
            label="Regime entry",
            choices=regime_choices,
            required=False,
            # setting id for javascript to use
            widget=forms.SelectMultiple(attrs={"id": "regime_entry"}),
        )
        self.fields["countries"] = forms.MultipleChoiceField(
            label="Country",
            choices=country_choices,
            required=False,
            # setting id for javascript to use
            widget=forms.SelectMultiple(attrs={"id": "countries"}),
        )
        self.fields["assigned_queues"] = forms.MultipleChoiceField(
            label="Assigned queues",
            choices=assigned_queues_choices,
            required=False,
            # setting id for javascript to use
            widget=forms.SelectMultiple(attrs={"id": "assigned-queues"}),
        )

        case_filters = [
            "case_reference",
            "status",
            "case_officer",
            "assigned_user",
            "export_type",
            "includes_refusal_recommendation_from_ogd",
            "submitted_from",
            "submitted_to",
            "flags",
            "finalised_from",
            "finalised_to",
        ]
        if queue.get("is_system_queue"):
            case_filters.append("assigned_queues")

        # When filters are cleared we need to reset all filter fields. Ideally we should do this
        # in clean() but we are posting anything in this form so we are just redirecting it to the
        # current queue which removes all query params.
        # Url doesn't include queue hence generating like this
        clear_filters_url = f'/queues/{queue["id"]}/'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            "return_to",
            Accordion(
                AccordionSection(
                    "Case",
                    *case_filters,
                    css_id="accordion-case-filters",
                ),
                AccordionSection(
                    "Product",
                    "control_list_entry",
                    "exclude_control_list_entry",
                    "regime_entry",
                    "exclude_regime_entry",
                    "report_summary",
                    "product_name",
                    "max_total_value",
                    "is_trigger_list",
                    "is_nca_applicable",
                ),
                AccordionSection(
                    "Applicant",
                    "organisation_name",
                    "exporter_site_name",
                    "goods_starting_point",
                ),
                AccordionSection(
                    "Parties",
                    "countries",
                    "party_name",
                    "exclude_denial_matches",
                    "exclude_sanction_matches",
                ),
                css_id="accordion-1",
            ),
            Fieldset(
                Submit("submit", "Apply filters", css_id="button-apply-filters"),
                Button(
                    "save_filter",
                    "Save filter",
                    css_id="button-save-filters",
                    formmethod="POST",
                    formaction=reverse("bookmarks:add_bookmark"),
                ),
                HTML(
                    f'<a href="{clear_filters_url}" class="govuk-button govuk-button--secondary" id="button-clear-filters">Clear filters</a>'  # noqa
                ),
                css_class="case-filter-actions",
            ),
        )
