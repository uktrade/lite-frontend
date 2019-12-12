from lite_forms.components import Form, Filter, Checkboxes

from sites.services import get_sites


def sites_form(request):
    return Form(
        title="Select locations",
        description="",
        questions=[Filter(), Checkboxes("sites", get_sites(request, request.user.organisation, True))],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        default_button_name="Save and continue",
    )
