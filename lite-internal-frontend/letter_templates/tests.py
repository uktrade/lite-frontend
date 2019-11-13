import json
from unittest import TestCase

from letter_templates.context_variables import get_context_variables, get_flattened_context_variables, JSON_PATH
from letter_templates.services import sort_letter_paragraphs
from letter_templates.templatetags.variable_highlight import ALT_OPEN_TAG, CLOSE_TAG, OPEN_TAG, variable_highlight


class SortLetterParagraphsTestCase(TestCase):
    def test_sort_letter_paragraphs(self):
        ids = ["abc", "def", "uvw", "xyz"]
        sorted_letter_paragraphs = sort_letter_paragraphs([
            {"id": "xyz", "label": "last"},
            {"id": "abc", "label": "first"},
            {"id": "uvw", "label": "third"},
            {"id": "def", "label": "second"},
            {"id": "klm", "label": "not in result"},
        ],
            ids + ["nop"],
        )
        result_ids = [paragraph["id"] for paragraph in sorted_letter_paragraphs]
        self.assertEqual(ids, result_ids)


class LetterTemplateEditLetterParagraphsTestCase(TestCase):
    def test_variable_highlight(self):
        """
        Ensure that variable_highlight returns the correct value
        """
        test_input = '{% if True %}{{ applicant.name }}{% endif %}' * 2
        expected_output = (ALT_OPEN_TAG + '{% if True %}' + CLOSE_TAG + OPEN_TAG +
                           '{{ applicant.name }}' + CLOSE_TAG + ALT_OPEN_TAG + '{% endif %}' + CLOSE_TAG) * 2

        self.assertEqual(variable_highlight(test_input), expected_output)


class ContextVariablesTestCase(TestCase):
    def setUp(self):
        self.context_variables = get_context_variables()
        self.flattened_context_variables = get_flattened_context_variables()
        with open(JSON_PATH, 'r') as f:
            self.context_variables_json = json.load(f)

    def _validate_variable_dict(self, dictionary):
        """
        Get each item in each containing dict and validate that the variable
        is inside the dict of variables we have about a given object.
        This happens recursively until all dicts have been checked.
        """
        for key, value in dictionary.items():
            if isinstance(value, dict):
                expected = self.variables_in_json[key]
                for item in expected:
                    self.assertTrue(item in value)
                self._validate_variable_dict(value)

    def _validate_flattened_variables(self, dictionary, path):
        """
        Append the current key to the path if the item is a dict to build up the
        full path to a variable i.e. `application.user.id`
        When the flattened variable path is complete (no longer is a dict) it will assert
        that the item is in flattened context variables.
        This happens recursively until each flattened variable is found and verified.
        """
        for key, value in dictionary.items():
            if isinstance(value, dict):
                if path:
                    self._validate_flattened_variables(value, path + '.' + key)
                else:
                    self._validate_flattened_variables(value, path + key)
            else:
                flattened_variable = path + '.' + key
                self.assertTrue(flattened_variable in self.flattened_context_variables)

    def test_build_context_variable_json(self):
        self.variables_in_json = {}
        for key, value in self.context_variables_json.items():
            if 'variables' in value:
                self.variables_in_json[key] = value['variables']
            else:
                self.variables_in_json[key] = {}

        self._validate_variable_dict(self.context_variables)

    def test_flatten_context_variables(self):
        self._validate_flattened_variables(self.context_variables, '')
