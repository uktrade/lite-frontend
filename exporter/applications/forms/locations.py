from django import forms
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Submit, Layout, HTML

from exporter.applications.components import back_to_task_list
from exporter.core.constants import HMRC, CaseTypes, LocationType
from exporter.core.services import get_countries, get_external_locations
from lite_content.lite_exporter_frontend import goods, strings, generic
from lite_content.lite_exporter_frontend.goods import NewLocationForm, LocationTypeForm
from lite_forms.common import country_question
from lite_forms.components import (
    Form,
    RadioButtons,
    Option,
    TextArea,
    Filter,
    Checkboxes,
    TextInput,
    FormGroup,
    HiddenField,
    BackLink,
)
from lite_forms.helpers import conditional
from exporter.organisation.sites.services import get_sites


class Locations:
    ORGANISATION = "organisation"
    EXTERNAL = "external"
    DEPARTED = "departed"


def which_location_form(application_id, application_type):
    return Form(
        title=goods.GoodsLocationForm.WHERE_ARE_YOUR_GOODS_LOCATED_TITLE,
        description=goods.GoodsLocationForm.WHERE_ARE_YOUR_GOODS_LOCATED_DESCRIPTION,
        questions=[
            RadioButtons(
                "choice",
                [
                    Option(
                        key=Locations.ORGANISATION,
                        value=goods.GoodsLocationForm.ONE_OF_MY_REGISTERED_SITES,
                        description=goods.GoodsLocationForm.NOT_AT_MY_REGISTERED_SITES_DESCRIPTION,
                    ),
                    Option(
                        key=Locations.EXTERNAL,
                        value=goods.GoodsLocationForm.NOT_AT_MY_REGISTERED_SITES,
                        description=goods.GoodsLocationForm.NOT_AT_MY_REGISTERED_SITES_DESCRIPTION,
                    ),
                    conditional(
                        application_type == HMRC,
                        Option(
                            key=Locations.DEPARTED,
                            value=goods.GoodsLocationForm.DEPARTED_THE_COUNTRY,
                            description=goods.GoodsLocationForm.DEPARTED_THE_COUNTRY_DESCRIPTION,
                            show_or=True,
                        ),
                    ),
                ],
            )
        ],
        default_button_name=strings.CONTINUE,
        back_link=back_to_task_list(application_id),
    )


def add_external_location(request):
    return Form(
        title=goods.GoodsLocationForm.EXTERNAL_LOCATION_TITLE,
        questions=[
            RadioButtons(
                "choice",
                [
                    Option("new", goods.GoodsLocationForm.EXTERNAL_LOCATION_NEW_LOCATION),
                    Option("preexisting", goods.GoodsLocationForm.EXTERNAL_LOCATION_PREEXISTING_LOCATION),
                ],
            )
        ],
        default_button_name=strings.CONTINUE,
        back_link=BackLink(url=request.GET.get("return_to")),
    )


def new_external_location_form(request, application_type=None, location_type=None):
    return FormGroup(
        forms=[
            conditional(
                (application_type in [CaseTypes.SICL, CaseTypes.OICL]),
                location_type_form(request, application_type),
            ),
            new_location_form(request, application_type, location_type),
        ]
    )


def location_type_form(request, application_type=None):
    return Form(
        title=LocationTypeForm.TITLE,
        description=LocationTypeForm.DESCRIPTION,
        questions=[
            HiddenField("application_type", application_type),
            RadioButtons(
                name="location_type",
                title="",
                options=[
                    Option(key="land_based", value=LocationTypeForm.LAND_BASED),
                    Option(key="sea_based", value=LocationTypeForm.SEA_BASED),
                ],
                classes=["govuk-radios--inline"],
            ),
        ],
        default_button_name=LocationTypeForm.CONTINUE,
        back_link=BackLink(url=request.GET.get("return_to")),
    )


def new_location_form(request, application_type, location_type):
    exclude = []
    if application_type in [CaseTypes.SITL, CaseTypes.SICL, CaseTypes.OICL]:
        exclude.append("GB")

    countries = get_countries(request, True, exclude)

    return Form(
        title=NewLocationForm.TITLE,
        description=NewLocationForm.DESCRIPTION,
        questions=[
            HiddenField(name="external_locations", value=""),
            TextInput(name="name", title=NewLocationForm.Name.TITLE),
            TextArea(
                name="address",
                title=conditional(
                    location_type == LocationType.SEA_BASED,
                    NewLocationForm.Address.SEA_BASED_TITLE,
                    NewLocationForm.Address.TITLE,
                ),
                description=conditional(
                    application_type == CaseTypes.SITL,
                    NewLocationForm.Address.SITL_DESCRIPTION,
                    conditional(
                        location_type == LocationType.SEA_BASED,
                        NewLocationForm.Address.SEA_BASED_DESCRIPTION,
                        NewLocationForm.Address.DESCRIPTION,
                    ),
                ),
            ),
            conditional(location_type != LocationType.SEA_BASED, country_question(prefix="", countries=countries)),
        ],
        default_button_name=strings.SAVE_AND_CONTINUE,
    )


def external_locations_form(request, application_type):
    exclude = []
    if application_type in [CaseTypes.SITL, CaseTypes.SICL, CaseTypes.OICL]:
        exclude.append("GB")

    return Form(
        title="Select locations",
        questions=[
            Filter(),
            Checkboxes(
                name="external_locations[]",
                options=get_external_locations(
                    request, str(request.session["organisation"]), True, exclude, application_type
                ),
                filterable=True,
            ),
        ],
        default_button_name=strings.SAVE_AND_CONTINUE,
    )


def sites_form(request, application_type):
    exclude = ""
    if application_type in [CaseTypes.SITL, CaseTypes.SICL, CaseTypes.OICL]:
        exclude = "GB"

    return Form(
        title="Select locations",
        questions=[
            Filter(),
            Checkboxes(
                name="sites[]",
                options=get_sites(request, request.session["organisation"], True, False, exclude),
                filterable=True,
            ),
        ],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )


class GoodsStartingPointForm(forms.Form):
    goods_starting_point = forms.ChoiceField(
        label="",
        widget=forms.RadioSelect,
        choices=[
            ("GB", "Great Britain"),
            ("NI", "Northern Ireland"),
        ],
        error_messages={
            "required": ["Select if the products will begin their export journey in Great Britain or Northern Ireland"]
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1("Where will the products begin their export journey?"),
            "goods_starting_point",
            HTML.details(
                "Help with where the products begin their journey",
                "<p>For physical products (including software stored on memory devices or hardcopy technology) this is "
                "the place where they are packed for export.</p>"
                "<p>For intangible items such as software and technology (for example those sent over the internet), "
                "this is the location of the official business premises of the individual who is permitting this activity.</p>",
            ),
            Submit("submit", "Continue"),
        )


class PermanentOrTemporaryExportForm(forms.Form):
    export_type = forms.ChoiceField(
        label="",
        widget=forms.RadioSelect,
        choices=[("permanent", "Yes"), ("temporary", "No, this is a temporary export")],
        error_messages={"required": ["Select yes if the products are being permanently exported"]},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1("Are the products being permanently exported?"),
            "export_type",
            Submit("submit", "Continue"),
        )


class GoodsRecipientsForm(forms.Form):
    goods_recipients = forms.ChoiceField(
        label="",
        widget=forms.RadioSelect,
        choices=[
            ("direct_to_end_user", "Directly to the end-user"),
            ("via_consignee", "To an end-user via a consignee"),
            ("via_consignee_and_third_parties", "To an end-user via a consignee, with additional third parties"),
        ],
        error_messages={"required": ["Select who the products are going to"]},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1("Who are the products going to?"),
            "goods_recipients",
            HTML.details(
                "Help with end user, consignee and third party",
                "<p>An end-user receives the products in the destination country. They either use the products "
                "themselves, resell from stock, or export them again to another country.</p>"
                "<p>A consignee receives the products and then delivers or sells them to the end-user.</p>"
                "<p>A third party is involved in the export but not regarded as a consignee, end-user or ultimate "
                "end-user, for example they might be an agent, broker, consultant or distributor.</p>"
                "<p>For products being exported again passed their first destination, there may also be an ultimate "
                "end-user. An ultimate end-user in a third country receives goods via an onward export from the end user.</p>",
            ),
            Submit("submit", "Continue"),
        )
