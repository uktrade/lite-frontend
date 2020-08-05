from lite_forms.generators import confirm_form
from lite_content.lite_internal_frontend.cases import Manage


def rerun_routing_rules_confirmation_form():
    return confirm_form(
        title=Manage.RerunRoutingRules.TITLE,
        confirmation_name="confirm",
        back_link_text=Manage.RerunRoutingRules.BACKLINK,
        back_url="#",
        yes_label=Manage.RerunRoutingRules.YES,
        no_label=Manage.RerunRoutingRules.NO,
        submit_button_text=Manage.RerunRoutingRules.SUBMIT_BUTTON,
        container="case",
    )
