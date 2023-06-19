from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Field, Fieldset, HTML, Submit, Button, Accordion, AccordionSection
from django import forms
from django.forms.widgets import HiddenInput
from django.urls import reverse

from core.forms.utils import coerce_str_to_bool
from core.forms.widgets import CheckboxInputSmall

SLA_DAYS_RANGE = 99


class CasesFiltersForm(forms.Form):

    case_reference = forms.CharField(
        label="Case reference",
        widget=forms.TextInput(attrs={"id": "case_reference"}),
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
        label="Exporter site name",
        required=False,
    )
    exporter_site_address = forms.CharField(
        label="Exporter site address",
        required=False,
    )
    party_name = forms.CharField(
        label="Party name",
        required=False,
    )
    party_address = forms.CharField(
        label="Party address",
        required=False,
    )
    goods_related_description = forms.CharField(
        label="Goods related description",
        required=False,
    )
    country = forms.CharField(
        label="Country",
        required=False,
    )
    regime_entry = forms.CharField(
        label="Regime entry",
        required=False,
    )
    submitted_from = DateInputField(
        label="Submitted from date",
        required=False,
    )
    submitted_to = DateInputField(
        label="Submitted to date",
        required=False,
    )
    finalised_from = DateInputField(
        label="Finalised from date",
        required=False,
    )
    finalised_to = DateInputField(
        label="Finalised to date",
        required=False,
    )

    def get_field_choices(self, filters_data, field):
        return [("", "Select")] + [(choice["key"], choice["value"]) for choice in filters_data.get(field, [])]

    def __init__(self, queue, filters_data, all_flags, all_cles, *args, **kwargs):
        super().__init__(*args, **kwargs)

        case_type_choices = self.get_field_choices(filters_data, "case_types")
        case_status_choices = self.get_field_choices(filters_data, "statuses")
        advice_type_choices = self.get_field_choices(filters_data, "advice_types")
        gov_user_choices = [("", "Select"), ("not_assigned", "Not assigned")] + [
            (choice["id"], choice["full_name"]) for choice in filters_data["gov_users"]
        ]

        sla_days_choices = [("", "Select")] + [(i, i) for i in range(SLA_DAYS_RANGE)]
        sla_sorted_choices = [("", "Select"), ("ascending", "Ascending"), ("descending", "Descending")]
        nca_choices = [(True, "Filter by Nuclear Cooperation Agreement")]
        trigger_list_guidelines_choices = [(True, "Filter by trigger list")]
        flags_choices = [(flag["id"], flag["name"]) for flag in all_flags]
        cle_choices = [(cle["rating"], cle["rating"]) for cle in all_cles]
        hidden_cases_choices = [(True, "Show hidden cases, including cases with open ECJU queries.")]

        self.fields["case_type"] = forms.ChoiceField(
            choices=case_type_choices,
            label="Case type",
            widget=forms.Select(attrs={"id": "case_type"}),
            required=False,
        )

        self.fields["status"] = forms.ChoiceField(
            choices=case_status_choices,
            label="Case status",
            required=False,
        )

        self.fields["case_officer"] = forms.ChoiceField(
            choices=gov_user_choices,
            label="Case officer",
            required=False,
        )

        self.fields["assigned_user"] = forms.ChoiceField(
            choices=gov_user_choices,
            label="Assigned user",
            required=False,
        )

        self.fields["team_advice_type"] = forms.ChoiceField(
            label="Team advice type",
            choices=advice_type_choices,
            required=False,
        )

        self.fields["final_advice_type"] = forms.ChoiceField(
            label="Final advice type",
            choices=advice_type_choices,
            required=False,
        )

        self.fields["max_sla_days_remaining"] = forms.ChoiceField(
            label="Max SLA days remaining",
            choices=sla_days_choices,
            required=False,
        )

        self.fields["min_sla_days_remaining"] = forms.ChoiceField(
            label="Min SLA days remaining",
            choices=sla_days_choices,
            required=False,
        )

        self.fields["sla_days_elapsed"] = forms.ChoiceField(
            label="SLA days elapsed",
            choices=sla_days_choices,
            required=False,
        )

        self.fields["sla_days_elapsed_sort_order"] = forms.ChoiceField(
            label="Sorted by SLA days",
            choices=sla_sorted_choices,
            required=False,
        )
        self.fields["flags"] = forms.MultipleChoiceField(
            label="Flags",
            choices=flags_choices,
            required=False,
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
        self.fields["is_nca_applicable"] = forms.TypedChoiceField(
            choices=nca_choices,
            coerce=coerce_str_to_bool,
            label="",
            widget=CheckboxInputSmall(),
            required=False,
        )
        self.fields["is_trigger_list"] = forms.TypedChoiceField(
            choices=trigger_list_guidelines_choices,
            coerce=coerce_str_to_bool,
            label="",
            widget=CheckboxInputSmall(),
            required=False,
        )
        self.fields["hidden"] = forms.TypedChoiceField(
            choices=hidden_cases_choices,
            coerce=coerce_str_to_bool,
            label="",
            widget=CheckboxInputSmall(),
            required=False,
        )
        self.fields["return_to"] = forms.CharField(
            label="",
            widget=HiddenInput(),
            required=False,
        )

        case_filters = [
            "case_reference",
            "case_type",
            "status",
            "case_officer",
            "assigned_user",
            "return_to",
            Field("submitted_from"),
            Field("submitted_to"),
            Field.select("flags"),
            Field("finalised_from"),
            Field("finalised_to"),
        ]
        if not queue.get("is_system_queue"):
            case_filters.append("hidden")

        # When filters are cleared we need to reset all filter fields. Ideally we should do this
        # in clean() but we are posting anything in this form so we are just redirecting it to the
        # current queue which removes all query params.
        # Url doesn't include queue hence generating like this
        clear_filters_url = f'/queues/{queue["id"]}/'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Accordion(
                AccordionSection(
                    "Case",
                    *case_filters,
                    css_id="accordion-case-filters",
                ),
                AccordionSection(
                    "Product",
                    Field.select("control_list_entry", id="control_list_entry"),
                    Field.text("regime_entry"),
                    Field.text("goods_related_description"),
                    Field("is_trigger_list"),
                    Field("is_nca_applicable"),
                ),
                AccordionSection(
                    "Applicant",
                    Field.text("exporter_application_reference"),
                    Field.text("organisation_name"),
                    Field.text("exporter_site_name"),
                    Field.text("exporter_site_address"),
                ),
                AccordionSection(
                    "Parties",
                    Field.text("party_name"),
                    Field.text("party_address"),
                    Field.text("country"),
                ),
                AccordionSection(
                    "Misc",
                    Field.select("team_advice_type"),
                    Field.select("final_advice_type"),
                    Field.select("max_sla_days_remaining"),
                    Field.select("min_sla_days_remaining"),
                    Field.select("sla_days_elapsed"),
                    Field.select("sla_days_elapsed_sort_order"),
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
