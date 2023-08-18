from caseworker.cases.views.finalisation.forms import SelectInformLetterTemplateForm, LetterEditTextForm


def test_select_letter_template_form():
    template_paragraphs = [("id1", "display 1"), ("id2", "display 2"), ("id3", "display3")]
    form = SelectInformLetterTemplateForm(
        inform_paragraphs=template_paragraphs,
        data={"select_template": "id1"},
    )
    assert form.is_valid() is True


def test_select_letter_template_form_not_valid():
    template_paragraphs = [("id1", "display 1"), ("id2", "display 2"), ("id3", "display3")]
    form = SelectInformLetterTemplateForm(inform_paragraphs=template_paragraphs, data={})
    assert form.is_valid() == False
    assert form.errors == {"select_template": ["please select a template"]}


def test_letter_edit_form():
    form = LetterEditTextForm(
        data={"text": "not in agreement"},
    )
    assert form.is_valid() is True


def test_letter_edit_form_not_valid():
    form = LetterEditTextForm(data={})

    assert form.is_valid() is False

    assert form.errors == {"text": ["Edit text is Required"]}
