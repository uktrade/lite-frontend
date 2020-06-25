from django.urls import reverse_lazy

from conf.constants import Permissions
from core.services import get_countries, get_organisation_users
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
from organisation.sites.services import get_sites, filter_sites_in_the_uk


def new_site_forms(request):
    in_uk = request.POST.get("location", "").lower() == "united_kingdom"

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
                        in_uk, address_questions(None), foreign_address_questions(get_countries(request, True, ["GB"])),
                    ),
                    HiddenField("validate_only", True),
                ],
                default_button_name=generic.CONTINUE,
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
                            request.user.organisation,
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
                                                get_sites(request, request.user.organisation)
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
                            for site in filter_sites_in_the_uk(get_sites(request, request.user.organisation))
                        ],
                    ),
                ],
            ),
            HiddenField("validate_only", True),
            HiddenField("records_located_step", True),
        ],
        default_button_name=generic.CONTINUE,
    )
