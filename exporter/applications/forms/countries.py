from exporter.applications.components import back_to_task_list
from exporter.applications.helpers.countries import ContractTypes
from exporter.core.services import get_countries
from lite_content.lite_exporter_frontend import strings
from lite_content.lite_exporter_frontend.applications import ContractTypes as contractTypeStrings
from lite_forms.components import Form, Filter, Checkboxes, RadioButtons, Option, TextInput, HiddenField


def countries_form(request, application_id):
    return Form(
        title=strings.applications.DestinationForm.TITLE,
        description="",
        questions=[
            Filter(),
            Checkboxes(
                name="countries[]",
                options=get_countries(request, True, ["GB"]),
                classes=["govuk-checkboxes--small"],
                show_select_links=True,
                filterable=True,
            ),
        ],
        default_button_name=strings.SAVE_AND_CONTINUE,
        back_link=back_to_task_list(application_id),
    )


def choose_contract_type_form():
    return Form(
        title=contractTypeStrings.ChooseContractTypeForm.TITLE,
        description="Examples of sectors and contract types are ‘army’, ‘registered firearm dealers’ and ‘for the exporters own use’.",
        questions=[
            RadioButtons(
                "choice",
                [
                    Option("all", contractTypeStrings.ChooseContractTypeForm.ALL_COUNTRIES_OPTION),
                    Option("individual", contractTypeStrings.ChooseContractTypeForm.EACH_COUNTRY_INDIVIDUALLY_OPTION),
                ],
            )
        ],
        default_button_name=strings.SAVE,
        back_link=None,
    )


def contract_type_per_country_form(current_country, country_name):
    return Form(
        title=contractTypeStrings.AddContractTypesForm.TITLE + country_name,
        description="",
        questions=[
            HiddenField("countries", current_country),
            Checkboxes(
                name="contract_types[]",
                options=[
                    Option(key=key.value, value=ContractTypes.get_str_representation(key)) for key in ContractTypes
                ],
                classes=["govuk-checkboxes--small"],
                filterable=True,
            ),
            TextInput(name="other_contract_type_text", title=contractTypeStrings.AddContractTypesForm.PROVIDE_DETAILS),
        ],
        default_button_name=strings.SAVE_AND_CONTINUE,
    )
