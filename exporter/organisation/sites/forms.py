from django.urls import reverse_lazy
from django import forms
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit, Layout, HTML

from exporter.core.constants import Permissions
from exporter.core.services import get_countries, get_organisation_users
from lite_content.lite_exporter_frontend import strings, generic
from lite_content.lite_exporter_frontend.sites import AddSiteForm
from lite_forms.common import address_questions, foreign_address_questions
from lite_forms.components import (
    Heading,
    BackLink,
    Form,
    TextInput,
    RadioButtons,
    Option,
    FormGroup,
    HiddenField,
    Checkboxes,
    Filter,
    Label,
)
from lite_forms.helpers import conditional
from lite_forms.styles import HeadingStyle
from core.forms import widgets
from exporter.organisation.sites.services import get_sites, filter_sites_in_the_uk, validate_sites


class SiteFormMixin:
    @property
    def serialized_data(self):
        data = self.cleaned_data.copy()
        return data

    def add_form_errors(self, errors):
        for key, value in errors.items():
            if key in self.declared_fields:
                self.add_error(key, value)

    def clean(self):
        response = validate_sites(self.request, self.request.session["organisation"], self.serialized_data)
        json = response.json()
        if json.get("errors"):
            errors = self.flatten_errors(json.get("errors"))
            self.add_form_errors(errors)
        return self.cleaned_data

    def flatten_errors(self, errors):
        if errors.get("address"):
            if isinstance(errors["address"], list):
                del errors["address"]
            elif isinstance(errors["address"], dict):
                return {**errors, **errors.pop("address")}
        return errors


class NewSiteLocationForm(SiteFormMixin, forms.Form):
    location = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[
            ("united_kingdom", AddSiteForm.WhereIsYourSiteBased.IN_THE_UK),
            ("abroad", AddSiteForm.WhereIsYourSiteBased.OUTSIDE_THE_UK),
        ],
        error_messages={"required": ["Select a location"]},
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(AddSiteForm.WhereIsYourSiteBased.TITLE),
            HTML.p(AddSiteForm.WhereIsYourSiteBased.DESCRIPTION),
            "location",
            Submit("submit", "Continue"),
        )


class NewSiteUKAddressForm(SiteFormMixin, forms.Form):
    name = forms.CharField(label=AddSiteForm.Details.NAME, required=False)
    address_line_1 = forms.CharField(label="Building and street", required=False)
    address_line_2 = forms.CharField(label="", required=False)
    city = forms.CharField(label="Town or city", required=False)
    region = forms.CharField(label="County or state", required=False)
    postcode = forms.CharField(label="Postcode", required=False)
    phone_number = forms.CharField(
        label="Phone number", help_text="For international numbers include the country code", required=False
    )
    website = forms.CharField(label="Website", required=False)

    @property
    def serialized_data(self):
        data = self.cleaned_data.copy()
        # address is a separate model so the serializer on lite-api expects it as a nested dictionary
        return {
            "name": data.get("name"),
            # BUG: phone_number and website are not actually saved on the site instance
            # they are saved on the organisation
            # so including them here does nothing at the moment
            "phone_number": data.get("phone_number"),
            "website": data.get("website"),
            "address": {
                "address_line_1": data.get("address_line_1"),
                "address_line_2": data.get("address_line_2"),
                "city": data.get("city"),
                "region": data.get("region"),
                "postcode": data.get("postcode"),
            },
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(AddSiteForm.Details.TITLE),
            HTML.p(AddSiteForm.Details.DESCRIPTION),
            "name",
            HTML.h2(AddSiteForm.Details.ADDRESS_HEADER_UK),
            "address_line_1",
            "address_line_2",
            "city",
            "region",
            "postcode",
            "phone_number",
            "website",
            Submit("submit", "Continue"),
        )


class NewSiteInternationalAddressForm(SiteFormMixin, forms.Form):
    name = forms.CharField(label=AddSiteForm.Details.NAME, required=False)
    address = forms.CharField(
        label="Address", widget=forms.Textarea(attrs={"class": "govuk-input--width-20", "rows": 6}), required=False
    )
    phone_number = forms.CharField(
        label="Phone number", help_text="For international numbers include the country code", required=False
    )
    website = forms.CharField(label="Website", required=False)
    country = forms.ChoiceField(
        choices=[], widget=widgets.Autocomplete(attrs={"id": "country-autocomplete"}), required=False
    )  # populated in __init__

    @property
    def serialized_data(self):
        data = self.cleaned_data.copy()
        return {
            "name": data.get("name"),
            "phone_number": data.get("phone_number"),
            "website": data.get("website"),
            "address": {"address": data.get("address"), "country": data.get("country"),},
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        countries = get_countries(self.request, False, ["GB"])
        country_choices = [("", "Select a country")] + [(country["id"], country["name"]) for country in countries]
        self.declared_fields["country"].choices = country_choices

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(AddSiteForm.Details.TITLE),
            HTML.p(AddSiteForm.Details.DESCRIPTION),
            "name",
            HTML.h2(AddSiteForm.Details.ADDRESS_HEADER_ABROAD),
            "address",
            "phone_number",
            "website",
            "country",
            Submit("submit", "Continue"),
        )


class NewSiteConfirmForm(SiteFormMixin, forms.Form):
    are_you_sure = forms.ChoiceField(
        label=AddSiteForm.Postcode.CONTROL_TITLE,
        choices=[(True, AddSiteForm.Postcode.YES), (False, AddSiteForm.Postcode.NO)],
        widget=forms.RadioSelect(),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        postcode = kwargs.pop("postcode")
        existing_sites = get_sites(self.request, self.request.session["organisation"], postcode=postcode)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(AddSiteForm.Postcode.TITLE),
            HTML.p(AddSiteForm.Postcode.DESCRIPTION.format(", ".join(site["name"] for site in existing_sites))),
            "are_you_sure",
            Submit("submit", "Continue"),
        )


class NewSiteAssignUsersForm(SiteFormMixin, forms.Form):
    users = forms.MultipleChoiceField(
        label="", choices=[], widget=forms.CheckboxSelectMultiple(), required=False,  # populated in __init__
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        organisation_members = get_organisation_users(
            self.request,
            self.request.session["organisation"],
            {"disable_pagination": True, "exclude_permission": Permissions.ADMINISTER_SITES},
            False,
        )
        users_choices = [
            (user["id"], f"{user['first_name']} {user['last_name']}" if user["first_name"] else user["email"])
            for user in organisation_members
        ]
        self.declared_fields["users"].choices = users_choices
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(AddSiteForm.AssignUsers.TITLE),
            HTML.p(AddSiteForm.AssignUsers.DESCRIPTION),
            HTML(render_to_string("forms/filter.html")) if users_choices else None,
            "users" if users_choices else HTML.warning("No items"),
            Submit("submit", "Continue"),
        )


def new_site_forms(request):
    is_individual = request.POST.get("type") == "individual"
    in_uk = request.POST.get("location", "").lower() == "united_kingdom"
    sites = []
    if request.POST.get("address.postcode"):
        sites = get_sites(request, request.session["organisation"], postcode=request.POST.get("address.postcode", ""))

    return FormGroup(
        [
            Form(
                caption="Step 1 of 4",
                title=AddSiteForm.WhereIsYourSiteBased.TITLE,
                description=AddSiteForm.WhereIsYourSiteBased.DESCRIPTION,
                questions=[
                    RadioButtons(
                        name="location",
                        options=[
                            Option(
                                key="united_kingdom",
                                value=AddSiteForm.WhereIsYourSiteBased.IN_THE_UK,
                                description=AddSiteForm.WhereIsYourSiteBased.IN_THE_UK_DESCRIPTION,
                            ),
                            Option(
                                key="abroad",
                                value=AddSiteForm.WhereIsYourSiteBased.OUTSIDE_THE_UK,
                                description=AddSiteForm.WhereIsYourSiteBased.OUTSIDE_THE_UK_DESCRIPTION,
                            ),
                        ],
                    )
                ],
                default_button_name=generic.CONTINUE,
                back_link=BackLink(AddSiteForm.BACK_LINK, reverse_lazy("organisation:sites:sites")),
            ),
            Form(
                caption="Step 2 of 4",
                title=AddSiteForm.Details.TITLE,
                description=AddSiteForm.Details.DESCRIPTION,
                questions=[
                    TextInput(title=AddSiteForm.Details.NAME, name="name"),
                    Heading(
                        conditional(
                            in_uk, AddSiteForm.Details.ADDRESS_HEADER_UK, AddSiteForm.Details.ADDRESS_HEADER_ABROAD
                        ),
                        HeadingStyle.M,
                    ),
                    *conditional(
                        in_uk,
                        address_questions(None, is_individual),
                        foreign_address_questions(is_individual, get_countries(request, True, ["GB"])),
                    ),
                    HiddenField("validate_only", True),
                ],
                default_button_name=generic.CONTINUE,
            ),
            conditional(
                sites,
                Form(
                    title=AddSiteForm.Postcode.TITLE,
                    description=AddSiteForm.Postcode.DESCRIPTION.format(", ".join(site["name"] for site in sites)),
                    questions=[
                        HiddenField(name="are_you_sure", value=None),
                        RadioButtons(
                            name="are_you_sure",
                            title=AddSiteForm.Postcode.CONTROL_TITLE,
                            options=[Option(True, AddSiteForm.Postcode.YES), Option(False, AddSiteForm.Postcode.NO),],
                        ),
                    ],
                    default_button_name=generic.CONTINUE,
                ),
            ),
            site_records_location(request, in_uk),
            Form(
                caption="Step 4 of 4",
                title=AddSiteForm.AssignUsers.TITLE,
                description=AddSiteForm.AssignUsers.DESCRIPTION,
                questions=[
                    Filter(placeholder=AddSiteForm.AssignUsers.FILTER),
                    Checkboxes(
                        name="users[]",
                        options=get_organisation_users(
                            request,
                            request.session["organisation"],
                            {"disable_pagination": True, "exclude_permission": Permissions.ADMINISTER_SITES},
                            True,
                        ),
                        filterable=True,
                    ),
                    HiddenField("validate_only", False),
                ],
                default_button_name=generic.SAVE_AND_CONTINUE,
            ),
        ]
    )


def edit_site_name_form(site):
    return Form(
        title=strings.sites.SitesPage.EDIT + site["name"],
        questions=[TextInput(title="Name", name="name"),],
        back_link=BackLink(
            strings.sites.SitesPage.BACK_TO + site["name"],
            reverse_lazy("organisation:sites:site", kwargs={"pk": site["id"]}),
        ),
    )


def site_records_location(request, in_uk=True, is_editing=False):
    return Form(
        caption="" if is_editing else "Step 3 of 4",
        title=strings.sites.AddSiteForm.SiteRecords.SiteInUK.TITLE
        if in_uk
        else strings.sites.AddSiteForm.SiteRecords.SiteNotInUK.TITLE,
        description=strings.sites.AddSiteForm.SiteRecords.DESCRIPTION,
        questions=[
            *conditional(
                in_uk,
                [
                    RadioButtons(
                        name="site_records_stored_here",
                        options=[
                            Option(key=True, value=strings.YES),
                            Option(
                                key=False,
                                value=strings.sites.AddSiteForm.SiteRecords.SiteInUK.NO_RECORDS_HELD_ELSEWHERE,
                                components=[
                                    RadioButtons(
                                        name="site_records_located_at",
                                        options=[
                                            Option(site["id"], site["name"])
                                            for site in filter_sites_in_the_uk(
                                                get_sites(request, request.session["organisation"])
                                            )
                                        ],
                                    ),
                                    Label(
                                        'If the site isn\'t listed, you need to <a id="site-dashboard" href="'
                                        + str(reverse_lazy("organisation:sites:sites"))
                                        + '" class="govuk-link govuk-link--no-visited-state">'
                                        + "add the site"
                                        + "</a> "
                                        + "from your account dashboard."
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
                [
                    HiddenField("site_records_stored_here", False),
                    Label(
                        'If the site isn\'t listed, you need to <a id="site-dashboard" href="'
                        + str(reverse_lazy("organisation:sites:sites"))
                        + '" class="govuk-link govuk-link--no-visited-state">'
                        + "add the site"
                        + "</a> "
                        + "from your account dashboard."
                    ),
                    RadioButtons(
                        name="site_records_located_at",
                        options=[
                            Option(site["id"], site["name"])
                            for site in filter_sites_in_the_uk(get_sites(request, request.session["organisation"]))
                        ],
                    ),
                ],
            ),
            HiddenField("validate_only", True),
            HiddenField("records_located_step", True),
        ],
        default_button_name=generic.CONTINUE,
    )
