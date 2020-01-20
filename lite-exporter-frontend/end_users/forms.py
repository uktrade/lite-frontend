from django.urls import reverse_lazy

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
from lite_forms.generators import success_page, confirm_form
from lite_forms.helpers import conditional

from core.services import get_countries


def apply_for_an_end_user_advisory_form(individual, commercial):
    return FormGroup(
        [
            Form(
                title="Confirm how your products will be used",
                questions=[
                    HTMLBlock(
                        "<ul class='govuk-list govuk-list--bullet'>"
                        "<li class='govuk-!-margin-bottom-5'>I've checked the <a class='govuk-link' href='https://scsanctions.un.org/fop/fop?xml=htdocs/resources/xml/en/consolidated.xml&xslt=htdocs/resources/xsl/en/consolidated.xsl'>UN Security Council Committee's list</a> and my products will not be used by anyone named on this list</li>"  # noqa
                        "<li class='govuk-!-margin-bottom-5'>I've checked the <a class='govuk-link' href='https://permissions-finder.service.trade.gov.uk/'>Department for International Trade's list of controlled goods</a> and my products are not controlled</li>"  # noqa
                        "<li class='govuk-!-margin-bottom-5'>I've previously not been informed by the Export Control Joint Unit (ECJU) that my products could be used to make chemical, biological or nuclear weapons</li>"  # noqa
                        "<li>I do not have any reason to suspect that my products could be used to make chemical, biological or nuclear weapons</li>"  # noqa
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
                        commercial, TextInput(title="Nature of the end user's business", name="nature_of_business"),
                    ),
                    conditional(not individual, TextInput(title="Contact's name", name="contact_name")),
                    conditional(not individual, TextInput(title="Job title", name="contact_job_title"),),
                    conditional(not individual, TextInput(title="Email address", name="contact_email"),),
                    conditional(not individual, TextInput(title="Telephone number", name="contact_telephone"),),
                    TextInput(title="Website address (optional)", name="end_user.website", optional=True),
                    TextArea(
                        title="Address",
                        description="The delivery address or registered office for the person "
                        "receiving the products.",
                        name="end_user.address",
                    ),
                    country_question(countries=get_countries(None, True), prefix="end_user."),
                    HiddenField("validate_only", True),
                ],
                default_button_name="Continue",
            ),
            Form(
                title="More information about the end user",
                questions=[
                    TextArea(
                        title="What's your reasoning behind this query? (optional)",
                        optional=True,
                        name="reasoning",
                        extras={"max_length": 2000},
                    ),
                    TextArea(
                        title="Is there any other information you can provide about the end user? (optional)",
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


def copy_end_user_advisory_form(individual, commercial):
    return FormGroup(
        [
            Form(
                title="End user details",
                questions=[
                    TextInput(title="Organisation name", name="end_user.name"),
                    conditional(individual, TextInput(title="Email address", name="contact_email")),
                    conditional(individual, TextInput(title="Telephone number", name="contact_telephone")),
                    conditional(
                        commercial, TextInput(title="Nature of the end user's business", name="nature_of_business"),
                    ),
                    conditional(not individual, TextInput(title="Contact's name", name="contact_name")),
                    conditional(not individual, TextInput(title="Job title", name="contact_job_title"),),
                    conditional(not individual, TextInput(title="Email address", name="contact_email"),),
                    conditional(not individual, TextInput(title="Telephone number", name="contact_telephone"),),
                    TextInput(title="Website address (optional)", name="end_user.website", optional=True),
                    TextArea(
                        title="Address",
                        description="The delivery address or registered office for the person "
                        "receiving the products",
                        name="end_user.address",
                    ),
                    country_question(countries=get_countries(None, True), prefix="end_user."),
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
                        title="What's your reasoning behind this query? (optional)",
                        optional=True,
                        name="reasoning",
                        extras={"max_length": 2000,},
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
        title="Advisory successfully submitted",
        secondary_title="Your reference number: " + query_reference,
        description="ECJU usually takes 2 " "working days to check an end user.",
        what_happens_next=["You'll receive an email from ECJU when the check is finished."],
        links={
            "View your end user advisories": reverse_lazy("end_users:end_users"),
            "Submit another end user advisory": reverse_lazy("end_users:apply"),
            "Return to your export control account dashboard": reverse_lazy("core:hub"),
        },
    )


def respond_to_query_form(query_id, ecju_query):
    return Form(
        title="Respond to end user advisory",
        description="",
        questions=[
            HTMLBlock(
                '<div class="app-ecju-query__text" style="display: block; max-width: 100%;">'
                + ecju_query["question"]
                + "</div><br><br>"
            ),
            TextArea(
                name="response",
                title="Your response",
                description="You can't edit the response once it's submitted.",
                extras={"max_length": 2200},
            ),
            HiddenField(name="form_name", value="respond_to_query"),
        ],
        back_link=BackLink(
            "Back to product",
            reverse_lazy("end_users:end_user_detail", kwargs={"pk": query_id, "type": "ecju-queries"}),
        ),
        default_button_name="Submit response",
    )


def ecju_query_respond_confirmation_form(edit_response_url):
    return confirm_form(
        title="Confirm you want to send the response",
        confirmation_name="confirm_response",
        hidden_field="ecju_query_response_confirmation",
        yes_label="Confirm and send the response",
        no_label="Cancel",
        back_link_text="Back to edit response",
        back_url=edit_response_url,
    )
