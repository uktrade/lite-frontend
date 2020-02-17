from applications.components import back_to_task_list
from conf.constants import HMRC
from core.services import get_countries, get_external_locations
from lite_content.lite_exporter_frontend import goods, strings
from lite_forms.components import Form, RadioButtons, Option, TextArea, Select, Filter, Checkboxes, TextInput
from lite_forms.helpers import conditional


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


def add_external_location():
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
    )


def new_location_form():
    return Form(
        title="Add an external location",
        questions=[
            TextInput(title="Name", name="name"),
            TextArea("address", "Address"),
            Select(title="Country", description="", name="country", options=get_countries(None, True)),
        ],
        default_button_name=strings.SAVE_AND_CONTINUE,
    )


def external_locations_form(request):
    return Form(
        title="Select locations",
        description="",
        questions=[
            Filter(),
            Checkboxes("external_locations", get_external_locations(request, str(request.user.organisation), True)),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        default_button_name=strings.SAVE_AND_CONTINUE,
    )
