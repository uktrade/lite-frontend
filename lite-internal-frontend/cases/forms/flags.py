from cases.helpers import case_view_breadcrumbs
from lite_content.lite_internal_frontend.flags import SetCaseFlagsForm, SetGenericFlagsForm
from lite_forms.components import Form, Filter, Checkboxes, TextArea, BackLink


def flags_form(flags, level, origin, url):
    return Form(
        title=SetGenericFlagsForm.TITLE,
        description=SetGenericFlagsForm.DESCRIPTION,
        questions=[
            Filter(placeholder=SetGenericFlagsForm.Filter.PLACEHOLDER),
            Checkboxes(name="flags", options=flags),
            TextArea(
                name="note",
                title=SetGenericFlagsForm.Note.TITLE,
                description=SetGenericFlagsForm.Note.DESCRIPTION + level,
                optional=True,
            ),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        back_link=BackLink(SetGenericFlagsForm.BACK + origin, url),
    )


def set_case_flags_form(flags, case):
    return Form(
        title=SetCaseFlagsForm.TITLE,
        description=SetCaseFlagsForm.DESCRIPTION,
        questions=[
            Filter(placeholder=SetCaseFlagsForm.Filter.PLACEHOLDER),
            Checkboxes(name="flags", options=flags),
            TextArea(
                name="note",
                title=SetCaseFlagsForm.Note.TITLE,
                description=SetCaseFlagsForm.Note.DESCRIPTION,
                optional=True,
            ),
        ],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        back_link=case_view_breadcrumbs(case, SetCaseFlagsForm.TITLE),
    )
