from http import HTTPStatus
from unittest import TestCase

from django.test.client import RequestFactory

from lite_forms.components import Form, DetailComponent, TextInput, FormGroup, Link
from lite_forms.helpers import (
    nest_data,
    flatten_data,
    remove_unused_errors,
    get_form_by_pk,
    get_next_form,
    get_previous_form,
    extract_links,
)
from lite_forms.submitters import submit_paged_form
from lite_forms.templatetags.custom_tags import prefix_dots


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

    def test_remove_unused_errors(self):
        form = Form(questions=[TextInput("name"), TextInput("age"), TextInput("password"), DetailComponent("", ""),])

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
                    "site": {"address": {"city": "London",}, "name": "Lemonworld",},
                },
                "user": {"first_name": "Matthew",},
            },
        )

    def test_flatten_data(self):
        value = {
            "reference": "conversation_16",
            "organisation": {
                "name": "Live on coffee and flowers inc.",
                "site": {"address": {"city": "London",}, "name": "Lemonworld",},
            },
            "user": {"first_name": "Matthew",},
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


class TestSubmitPagedFormTestCase(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

    def test_expect_many_values(self):
        """
        Ensure submit_paged_form handles a field which expects many values.
        """
        request = self.request_factory.post(
            "/thing",
            (
                "key_a=a&key_a=b&key_a=c&"
                "key_b=d&key_b=e&key_b=f&"
                "key_c=g&"
                "key_d=h&"
                "form_pk=0&"
                "csrfmiddlewaretoken=bar"
            ),
            content_type="application/x-www-form-urlencoded",
        )
        forms = FormGroup([Form(questions=[]), Form(questions=[]), Form(questions=[]),])

        def handle_post(request, data):
            return data, HTTPStatus.OK

        form, data = submit_paged_form(request, forms, handle_post, expect_many_values=["key_a", "key_c", "key_e"])

        self.assertEqual(
            data, {"key_a": ["a", "b", "c"], "key_b": "f", "key_c": ["g"], "key_d": "h", "key_e": [],},
        )


class TemplateTagsTestCase(TestCase):
    def test_prefix_dots(self):
        self.assertEqual("nodots", prefix_dots("nodots"))
        self.assertEqual(r"\\.startdot", prefix_dots(".startdot"))
        self.assertEqual(r"enddot\\.", prefix_dots("enddot."))
        self.assertEqual(r"mid\\.dot", prefix_dots("mid.dot"))
        self.assertEqual(r"\\.all\\.the\\.dots\\.", prefix_dots(".all.the.dots."))


class LabelMarkdownTest(TestCase):
    def test_links(self):
        output = extract_links(
            "This is [America](https://en.wikipedia.org/wiki/United_States)"
            "This is [United Kingdom](https://en.wikipedia.org/wiki/United_Kingdom)."
        )
        expected_output = [
            "This is ",
            Link("America", "https://en.wikipedia.org/wiki/United_States"),
            "This is ",
            Link("United Kingdom", "https://en.wikipedia.org/wiki/United_Kingdom"),
            ".",
        ]

        self.assertEqual(expected_output, output)

    def test_no_links(self):
        output = extract_links("Hello")
        expected_output = ["Hello"]

        self.assertEqual(expected_output, output)
