from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Field, Fieldset, HTML, Submit, Button, Accordion, AccordionSection
from django import forms
from django.forms.widgets import HiddenInput
from django.urls import reverse

from caseworker.queues.services import get_queues
from core.forms.utils import coerce_str_to_bool
from core.forms.widgets import CheckboxInputSmall

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
    control_list_entry = forms.CharField(
        label="Control list entry",
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

    def __init__(self, request, queue, filters_data, all_flags, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        assigned_queues_choices = [
            (queue["id"], f"{queue['team']['name']}: {queue['name']}")
            for queue in get_queues(request, convert_to_options=False, users_team_first=True)
        ]

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
        self.fields["assigned_queues"] = forms.MultipleChoiceField(
            label="Assigned queues",
            choices=assigned_queues_choices,
            required=False,
            # setting id for javascript to use
            widget=forms.SelectMultiple(attrs={"id": "assigned-queues"}),
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
        self.fields["return_to"] = forms.CharField(
            label="",
            widget=HiddenInput(),
            required=False,
        )

        case_filters = [
            "case_reference",
            "status",
            "case_officer",
            "assigned_user",
            "export_type",
            Field("submitted_from"),
            Field("submitted_to"),
            Field.select("flags"),
            Field("finalised_from"),
            Field("finalised_to"),
            "return_to",
        ]
        if queue.get("is_system_queue"):
            case_filters.append(Field.select("assigned_queues"))

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
                    Field.text("control_list_entry", id="control_list_entry"),
                    Field.text("regime_entry"),
                    Field.text("goods_related_description"),
                    Field("is_trigger_list"),
                    Field("is_nca_applicable"),
                ),
                AccordionSection(
                    "Applicant",
                    Field.text("organisation_name"),
                    Field.text("exporter_site_name"),
                    Field.select("goods_starting_point"),
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
