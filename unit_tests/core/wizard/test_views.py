import logging

from django import forms


from core.common.forms import BaseForm
from core.wizard.views import BaseSessionWizardView


class BaseFormWithLayoutTitle(BaseForm):
    class Layout:
        TITLE = "title_for_BaseFormWithLayoutTitle"

    def get_layout_fields(self):
        return ()


class FormWithGetTitle(forms.Form):
    def get_title(self):
        return "title_for_FormWithGetTitle"


class FormWithoutGetTitle(forms.Form):
    pass


class FormWithTitleButEmptyString(forms.Form):
    def get_title(self):
        return ""


class SessionWizardTitleTestViewSteps:
    BASE_FORM_WITH_LAYOUT = "BASE_FORM_WITH_LAYOUT"
    FORM_WITH_GET_TITLE = "FORM_WITH_GET_TITLE"
    FORM_WITHOUT_GET_TITLE = "FORM_WITHOUT_GET_TITLE"
    FORM_WITH_TITLE_BUT_EMPTY_STRING = "FORM_WITH_TITLE_BUT_EMPTY_STRING"


class SessionWizardTitleTestView(BaseSessionWizardView):
    form_list = [
        (SessionWizardTitleTestViewSteps.BASE_FORM_WITH_LAYOUT, BaseFormWithLayoutTitle),
        (SessionWizardTitleTestViewSteps.FORM_WITH_GET_TITLE, FormWithGetTitle),
        (SessionWizardTitleTestViewSteps.FORM_WITHOUT_GET_TITLE, FormWithoutGetTitle),
        (SessionWizardTitleTestViewSteps.FORM_WITH_TITLE_BUT_EMPTY_STRING, FormWithTitleButEmptyString),
    ]


def test_base_form_with_layout_title(client, rf):
    request = rf.post("/", {"wizard_goto_step": SessionWizardTitleTestViewSteps.BASE_FORM_WITH_LAYOUT})
    request.session = client.session
    view = SessionWizardTitleTestView.as_view()
    response = view(request)
    assert response.context_data["title"] == "title_for_BaseFormWithLayoutTitle"


def test_form_with_get_title(client, rf):
    request = rf.post("/", {"wizard_goto_step": SessionWizardTitleTestViewSteps.FORM_WITH_GET_TITLE})
    request.session = client.session
    view = SessionWizardTitleTestView.as_view()
    response = view(request)
    assert response.context_data["title"] == "title_for_FormWithGetTitle"


def test_form_without_get_title(client, rf, caplog):
    request = rf.post("/", {"wizard_goto_step": SessionWizardTitleTestViewSteps.FORM_WITHOUT_GET_TITLE})
    request.session = client.session
    view = SessionWizardTitleTestView.as_view()
    response = view(request)
    assert "title" not in response.context_data
    assert caplog.record_tuples == [("core.wizard.views", logging.WARNING, "No title set for `FormWithoutGetTitle`")]


def test_form_with_title_but_empty_string(client, rf, caplog):
    request = rf.post("/", {"wizard_goto_step": SessionWizardTitleTestViewSteps.FORM_WITH_TITLE_BUT_EMPTY_STRING})
    request.session = client.session
    view = SessionWizardTitleTestView.as_view()
    response = view(request)
    assert response.context_data["title"] == ""
    assert caplog.record_tuples == [
        ("core.wizard.views", logging.WARNING, "Title set but blank for `FormWithTitleButEmptyString`")
    ]
