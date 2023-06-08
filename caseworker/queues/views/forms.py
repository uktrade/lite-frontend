from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Field, Fieldset, HTML, Submit, Button
from django import forms
from django.forms.widgets import HiddenInput
from django.urls import reverse

from caseworker.flags.services import get_flags
from core.forms.utils import coerce_str_to_bool
from core.forms.widgets import CheckboxInputSmall
from core.forms.layouts import ExpandingFieldset

SLA_DAYS_RANGE = 99


class CasesFiltersForm(forms.Form):

    case_reference = forms.CharField(
        label="Filter by case reference",
        widget=forms.TextInput(attrs={"id": "case_reference"}),
        required=False,
    )
    exporter_application_reference = forms.CharField(
        label="Filter by exporter reference",
        required=False,
    )
    organisation_name = forms.CharField(
        label="Filter by organisation name",
        required=False,
    )
    exporter_site_name = forms.CharField(
        label="Filter by exporter site name",
        required=False,
    )
    exporter_site_address = forms.CharField(
        label="Filter by exporter site address",
        required=False,
    )
    party_name = forms.CharField(
        label="Filter by party name",
        required=False,
    )
    party_address = forms.CharField(
        label="Filter by party address",
        required=False,
    )
    goods_related_description = forms.CharField(
        label="Filter by goods related description",
        required=False,
    )
    country = forms.CharField(
        label="Filter by country",
        required=False,
    )
    control_list_entry = forms.CharField(
        label="Filter by control list entry",
        required=False,
    )
    regime_entry = forms.CharField(
        label="Filter by regime entry",
        required=False,
    )
    submitted_from = DateInputField(
        label="Filter by submitted from date",
        required=False,
    )
    submitted_to = DateInputField(
        label="Filter by submitted to date",
        required=False,
    )
    finalised_from = DateInputField(
        label="Filter by finalised from date",
        required=False,
    )
    finalised_to = DateInputField(
        label="Filter by finalised to date",
        required=False,
    )

    def get_field_choices(self, filters_data, field):
        return [("", "Select")] + [(choice["key"], choice["value"]) for choice in filters_data.get(field, [])]

    def __init__(self, request, queue, filters_data, *args, **kwargs):
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
        flags_choices = [(flag["id"], flag["name"]) for flag in get_flags(request, disable_pagination=True)]
        hidden_cases_choices = [(True, "Show hidden cases, including cases with open ECJU queries.")]

        self.fields["case_type"] = forms.ChoiceField(
            choices=case_type_choices,
            label="Filter by type",
            widget=forms.Select(attrs={"id": "case_type"}),
            required=False,
        )

        self.fields["status"] = forms.ChoiceField(
            choices=case_status_choices,
            label="Filter by status",
            required=False,
        )

        self.fields["case_officer"] = forms.ChoiceField(
            choices=gov_user_choices,
            label="Filter by case officer",
            required=False,
        )

        self.fields["assigned_user"] = forms.ChoiceField(
            choices=gov_user_choices,
            label="Filter by assigned user",
            required=False,
        )

        self.fields["team_advice_type"] = forms.ChoiceField(
            label="Filter by team advice type",
            choices=advice_type_choices,
            required=False,
        )

        self.fields["final_advice_type"] = forms.ChoiceField(
            label="Filter by final advice type",
            choices=advice_type_choices,
            required=False,
        )

        self.fields["max_sla_days_remaining"] = forms.ChoiceField(
            label="Filter by max SLA days remaining",
            choices=sla_days_choices,
            required=False,
        )

        self.fields["min_sla_days_remaining"] = forms.ChoiceField(
            label="Filter by min SLA days remaining",
            choices=sla_days_choices,
            required=False,
        )

        self.fields["sla_days_elapsed"] = forms.ChoiceField(
            label="Filter by SLA days elapsed",
            choices=sla_days_choices,
            required=False,
        )

        self.fields["sla_days_elapsed_sort_order"] = forms.ChoiceField(
            label="Filter by sorted by SLA days",
            choices=sla_sorted_choices,
            required=False,
        )
        self.fields["flags"] = forms.MultipleChoiceField(
            label="Filter by flags",
            choices=flags_choices,
            required=False,
            # setting id for javascript to use
            widget=forms.SelectMultiple(attrs={"id": "flags"}),
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

        basic_filters = ["case_reference", "case_type", "status", "case_officer", "assigned_user", "return_to"]
        if not queue.get("is_system_queue"):
            basic_filters.append("hidden")

        # When filters are cleared we need to reset all filter fields. Ideally we should do this
        # in clean() but we are posting anything in this form so we are just redirecting it to the
        # current queue which removes all query params.
        # Url doesn't include queue hence generating like this
        clear_filters_url = f'/queues/{queue["id"]}/'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                *basic_filters,
                css_id="basic-filter-fields",
                css_class="basic-filter-fields",
            ),
            ExpandingFieldset(
                Field.text("exporter_application_reference"),
                Field.text("organisation_name"),
                Field.text("exporter_site_name"),
                Field.text("exporter_site_address"),
                Field.select("team_advice_type"),
                Field.select("final_advice_type"),
                Field.select("max_sla_days_remaining"),
                Field.select("min_sla_days_remaining"),
                Field.select("sla_days_elapsed"),
                Field.select("sla_days_elapsed_sort_order"),
                Field.text("party_name"),
                Field.text("party_address"),
                Field.text("goods_related_description"),
                Field.text("country"),
                Field.text("control_list_entry", id="control_list_entry"),
                Field.text("regime_entry"),
                Field.select("flags"),
                Field("submitted_from"),
                Field("submitted_to"),
                Field("finalised_from"),
                Field("finalised_to"),
                Field("is_nca_applicable"),
                Field("is_trigger_list"),
                legend="Advanced filters",
                css_id="advanced-filter-fields",
                css_class="advanced-group",
                text_div_css_class="advanced-filter-fields",
                details_id="advanced-filter-details",
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
                    f'<a href="{clear_filters_url}" class="govuk-button govuk-button--secondary govuk-button--secondary-white" id="button-clear-filters">Clear filters</a>'  # noqa
                ),
                css_class="case-filter-actions",
            ),
        )
