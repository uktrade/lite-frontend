from applications.components import back_to_task_list
from conf.constants import HMRC, CaseTypes, LocationType
from core.services import get_countries, get_external_locations
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
from organisation.sites.services import get_sites


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
        back_link=BackLink(url=request.GET.get("return_to_link")),
    )


def new_external_location_form(request, application_type=None, location_type=None):
    return FormGroup(
        forms=[
            conditional(
                (application_type in [CaseTypes.SICL, CaseTypes.OICL]), location_type_form(request, application_type),
            ),
            new_location_form(application_type, location_type),
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
        back_link=BackLink(url=request.GET.get("return_to_link")),
    )


def new_location_form(application_type, location_type):
    exclude = []
    if application_type in [CaseTypes.SITL, CaseTypes.SICL, CaseTypes.OICL]:
        exclude.append("GB")

    countries = get_countries(None, True, exclude)

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
            conditional(location_type != LocationType.SEA_BASED, country_question(prefix="", countries=countries),),
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
                    request, str(request.user.organisation), True, exclude, application_type
                ),
            ),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        default_button_name=strings.SAVE_AND_CONTINUE,
    )


def sites_form(request, application_type):
    exclude = []
    if application_type in [CaseTypes.SITL, CaseTypes.SICL, CaseTypes.OICL]:
        exclude.append("GB")

    return Form(
        title="Select locations",
        questions=[
            Filter(),
            Checkboxes(name="sites[]", options=get_sites(request, request.user.organisation, True, False, exclude)),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        default_button_name=generic.SAVE_AND_CONTINUE,
    )
