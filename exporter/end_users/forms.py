from django.urls import reverse_lazy

from exporter.core.services import get_countries
from lite_content.lite_exporter_frontend import strings
from lite_forms.common import country_question
from lite_forms.components import (
    RadioButtons,
    Form,
    Option,
    TextArea,
    TextInput,
    FormGroup,
    HiddenField,
    HTMLBlock,
    BackLink,
)
from lite_forms.generators import success_page
from lite_forms.helpers import conditional


def apply_for_an_end_user_advisory_form(request, individual, commercial):
    return FormGroup(
        [
            Form(
                title="Confirm how the products will be used",
                questions=[
                    HTMLBlock(
                        "<ul class='govuk-list govuk-list--bullet'>"
                        "<li class='govuk-!-margin-bottom-5'>I've checked the <a class='govuk-link' href='https://scsanctions.un.org/fop/fop?xml=htdocs/resources/xml/en/consolidated.xml&xslt=htdocs/resources/xsl/en/consolidated.xsl'>UN Security Council Committee's list</a> and the products will not be used by anyone named on this list</li>"  # noqa
                        "<li class='govuk-!-margin-bottom-5'>I've checked the <a class='govuk-link' href='https://permissions-finder.service.trade.gov.uk/'>Department for International Trade's list of controlled goods</a> and the products are not controlled</li>"  # noqa
                        "<li class='govuk-!-margin-bottom-5'>I've previously not been informed by the Export Control Joint Unit (ECJU) that the products could be used to make chemical, biological or nuclear weapons</li>"  # noqa
                        "<li>I do not have any reason to suspect that the products could be used to make chemical, biological or nuclear weapons</li>"  # noqa
                        "</ul>"
                    ),
                ],
                default_button_name="Confirm and continue",
            ),
            Form(
                title="Select the type of end user",
                questions=[
                    RadioButtons(
                        title="",
                        name="end_user.sub_type",
                        options=[
                            Option("government", "Government organisation"),
                            Option("commercial", "Commercial organisation"),
                            Option("individual", "An individual"),
                            Option("other", "Other", show_or=True),
                        ],
                    ),
                ],
                default_button_name="Continue",
            ),
            Form(
                title="End user details",
                questions=[
                    TextInput(title="Organisation name", name="end_user.name"),
                    conditional(individual, TextInput(title="Email address", name="contact_email")),
                    conditional(individual, TextInput(title="Telephone number", name="contact_telephone")),
                    conditional(
                        commercial,
                        TextInput(title="Nature of the end user's business", name="nature_of_business"),
                    ),
                    conditional(not individual, TextInput(title="Contact's name", name="contact_name")),
                    conditional(
                        not individual,
                        TextInput(title="Job title", name="contact_job_title"),
                    ),
                    conditional(
                        not individual,
                        TextInput(title="Email address", name="contact_email"),
                    ),
                    conditional(
                        not individual,
                        TextInput(title="Telephone number", name="contact_telephone"),
                    ),
                    TextInput(title="Website address", name="end_user.website", optional=True),
                    TextArea(
                        title="Address",
                        description="The delivery address or registered office for the person "
                        "receiving the products.",
                        name="end_user.address",
                    ),
                    country_question(countries=get_countries(request, True), prefix="end_user."),
                    HiddenField("validate_only", True),
                ],
                default_button_name="Continue",
            ),
            Form(
                title="More information about the end user",
                questions=[
                    TextArea(
                        title="What's your reasoning behind this query?",
                        optional=True,
                        name="reasoning",
                        extras={"max_length": 2000},
                    ),
                    TextArea(
                        title="Is there any other information you can provide about the end user?",
                        description="This may help provide a quicker response from ECJU.",
                        optional=True,
                        name="note",
                        extras={"max_length": 2000},
                    ),
                    HiddenField("validate_only", False),
                ],
            ),
        ],
        show_progress_indicators=True,
    )


def copy_end_user_advisory_form(request, individual, commercial):
    return FormGroup(
        [
            Form(
                title="End user details",
                questions=[
                    TextInput(title="Organisation name", name="end_user.name"),
                    conditional(individual, TextInput(title="Email address", name="contact_email")),
                    conditional(individual, TextInput(title="Telephone number", name="contact_telephone")),
                    conditional(
                        commercial,
                        TextInput(title="Nature of the end user's business", name="nature_of_business"),
                    ),
                    conditional(not individual, TextInput(title="Contact's name", name="contact_name")),
                    conditional(
                        not individual,
                        TextInput(title="Job title", name="contact_job_title"),
                    ),
                    conditional(
                        not individual,
                        TextInput(title="Email address", name="contact_email"),
                    ),
                    conditional(
                        not individual,
                        TextInput(title="Telephone number", name="contact_telephone"),
                    ),
                    TextInput(title="Website address", name="end_user.website", optional=True),
                    TextArea(
                        title="Address",
                        description="The delivery address or registered office for the person "
                        "receiving the products",
                        name="end_user.address",
                    ),
                    country_question(countries=get_countries(request, True), prefix="end_user."),
                    HiddenField("validate_only", True),
                ],
                back_link=BackLink(
                    strings.end_users.CopyEndUserAdvisoryForm.BACK_LINK, reverse_lazy("end_users:end_users")
                ),
                default_button_name=strings.CONTINUE,
            ),
            Form(
                title="More information about the end user",
                questions=[
                    TextArea(
                        title="What's your reasoning behind this query?",
                        optional=True,
                        name="reasoning",
                        extras={
                            "max_length": 2000,
                        },
                    ),
                    TextArea(
                        title="Is there any other information you can provide about the end user?",
                        description="This may help provide a quicker response from ECJU.",
                        optional=True,
                        name="note",
                        extras={"max_length": 2000},
                    ),
                    HiddenField("validate_only", False),
                ],
            ),
        ]
    )


def end_user_advisory_success_page(request, query_reference):
    return success_page(
        request=request,
        title="Advisory submitted",
        secondary_title="ECJU reference: " + query_reference,
        description="ECJU usually takes 2 working days to check an end user.",
        what_happens_next=["You'll receive an email from ECJU when the check is finished."],
        links={
            "View your end user advisories": reverse_lazy("end_users:end_users"),
            "Submit another end user advisory": reverse_lazy("end_users:apply"),
            "Return to your export control account dashboard": reverse_lazy("core:home"),
        },
    )
