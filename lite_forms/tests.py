from unittest import TestCase

from bs4 import BeautifulSoup
from django.template.loader import render_to_string

from lite_forms.components import (
    Form,
    DetailComponent,
    TextInput,
    FormGroup,
    Label,
    Option,
    BackLink,
    HiddenField,
    RadioButtons,
    FileUpload,
)
from lite_forms.helpers import (
    nest_data,
    flatten_data,
    remove_unused_errors,
    get_form_by_pk,
    get_next_form,
    get_previous_form,
    convert_form_to_summary_list_instance,
    get_all_form_components,
    insert_hidden_fields,
)
from lite_forms.templatetags import custom_tags
from lite_forms.templatetags.custom_tags import prefix_dots
from lite_forms.views import FormView


class FormViewTests(TestCase):
    def test_parse_boolean(self):
        parse_boolean = FormView().parse_boolean
        assert parse_boolean(True) == True
        assert parse_boolean(False) == False
        assert parse_boolean("yes") == True
        assert parse_boolean("no") == False
        assert parse_boolean("YES") == True
        assert parse_boolean("NO") == False
        assert parse_boolean("true") == True
        assert parse_boolean("false") == False


class FormTests(TestCase):
    def test_get_form_by_pk(self):
        forms = FormGroup([Form(questions=[]), Form(questions=[]), Form(questions=[])])

        self.assertEqual(get_form_by_pk(1, forms).pk, 1)

    def test_get_previous_form_by_pk(self):
        forms = FormGroup([Form(questions=[]), Form(questions=[]), Form(questions=[])])

        self.assertEqual(get_previous_form(2, forms).pk, 1)

    def test_get_next_form_by_pk(self):
        forms = FormGroup([Form(questions=[]), Form(questions=[]), Form(questions=[])])

        self.assertEqual(get_next_form(1, forms).pk, 2)

    def test_classname(self):
        expected_value = "type"
        actual_value = custom_tags.classname(TestCase)

        self.assertEqual(actual_value, expected_value)

    def test_remove_unused_errors(self):
        form = Form(
            questions=[
                TextInput("name"),
                TextInput("age"),
                TextInput("password"),
                DetailComponent("", ""),
            ]
        )

        errors = {
            "name": "This field must not be empty",
            "email": "This field must not be empty",
            "age": "This field must not be empty",
            "password": "This field must not be empty",
        }

        cleaned_errors = {
            "name": "This field must not be empty",
            "age": "This field must not be empty",
            "password": "This field must not be empty",
        }

        self.assertEqual(cleaned_errors, remove_unused_errors(errors, form))

    def test_nest_data(self):
        value = {
            "reference": "conversation_16",
            "organisation.name": "Live on coffee and flowers inc.",
            "organisation.site.address.city": "London",
            "organisation.site.name": "Lemonworld",
            "user.first_name": "Matthew",
        }

        data = nest_data(value)

        self.assertEqual(
            data,
            {
                "reference": "conversation_16",
                "organisation": {
                    "name": "Live on coffee and flowers inc.",
                    "site": {
                        "address": {
                            "city": "London",
                        },
                        "name": "Lemonworld",
                    },
                },
                "user": {
                    "first_name": "Matthew",
                },
            },
        )

    def test_flatten_data(self):
        value = {
            "reference": "conversation_16",
            "organisation": {
                "name": "Live on coffee and flowers inc.",
                "site": {
                    "address": {
                        "city": "London",
                    },
                    "name": "Lemonworld",
                },
            },
            "user": {
                "first_name": "Matthew",
            },
        }

        data = flatten_data(value)

        self.assertEqual(
            data,
            {
                "reference": "conversation_16",
                "organisation.name": "Live on coffee and flowers inc.",
                "organisation.site.address.city": "London",
                "organisation.site.name": "Lemonworld",
                "user.first_name": "Matthew",
            },
        )

    def test_convert_form_to_summary_list_instance(self):
        form = Form(title="I Am Easy to Find", caption="The National", default_button_name="Rylan")
        form = convert_form_to_summary_list_instance(form)
        self.assertEqual(form.caption, "The National")
        self.assertEqual(form.buttons[0].value, "Save and return")
        self.assertEqual(form.buttons[0].action, "return")

    def test_get_all_form_components(self):
        form = Form(
            title="I Am Easy to Find",
            questions=[
                RadioButtons(
                    name="hello",
                    options=[
                        Option("key", "value", components=[TextInput("text")]),
                        Option("key2", "value", components=[TextInput("text2")]),
                    ],
                )
            ],
        )
        components = get_all_form_components(form)
        self.assertEqual(len(components), 3)

    def test_insert_hidden_fields(self):
        form = Form(
            title="I Am Easy to Find",
            questions=[],
        )
        insert_hidden_fields({"matt": "berninger"}, form)
        self.assertEqual(len(form.questions), 1)


class TemplateTagsTestCase(TestCase):
    def test_prefix_dots(self):
        self.assertEqual("nodots", prefix_dots("nodots"))
        self.assertEqual(r"\\.startdot", prefix_dots(".startdot"))
        self.assertEqual(r"enddot\\.", prefix_dots("enddot."))
        self.assertEqual(r"mid\\.dot", prefix_dots("mid.dot"))
        self.assertEqual(r"\\.all\\.the\\.dots\\.", prefix_dots(".all.the.dots."))


class SingleQuestionFormAccessibilityTest(TestCase):
    def test_no_questions_no_title_label(self):
        form = Form()
        self.assertIsNone(form.single_form_element)

    def test_no_user_inputs_no_title_label(self):
        form = Form(
            questions=[
                BackLink(),
                Label("abc"),
                HiddenField("abc", "123"),
            ]
        )
        self.assertIsNone(form.single_form_element)

    def test_single_user_input_with_other_questions_has_title_label(self):
        name = "Test"
        form = Form(
            questions=[
                BackLink(),
                Label("abc"),
                TextInput(name),
                HiddenField("abc", "123"),
            ]
        )
        self.assertEqual(form.single_form_element.name, name)

    def test_single_user_input_alone_has_title_label(self):
        name = "Test"
        form = Form(
            questions=[
                TextInput(name),
            ]
        )
        self.assertEqual(form.single_form_element.name, name)

    def test_multiple_user_inputs_no_title_label(self):
        form = Form(
            questions=[
                TextInput("abc"),
                TextInput("def"),
            ]
        )
        self.assertIsNone(form.single_form_element)


class FileUploadTest(TestCase):
    def test_file_upload_accept_props(self):
        """Test that vanilla FileUpload component is rendered with the right accept props."""
        form = Form("test-file-upload", "A form to test file upload component", [FileUpload()])
        html = render_to_string("form.html", {"page": form})
        soup = BeautifulSoup(html, "html.parser")
        accept = soup.find(id="file")["accept"].split(",")
        assert accept == [
            "application/pdf",
            "application/msword",
            "application/vnd.oasis.opendocument.text",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/rtf",
            "application/xml",
            "text/xml",
            "text/plain",
            "text/csv",
            "text/rtf",
            "text/msword",
            "image/jpeg",
            "image/png",
            "image/tiff",
        ]
