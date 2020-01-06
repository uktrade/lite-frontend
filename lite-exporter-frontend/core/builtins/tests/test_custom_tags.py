from django.test import TestCase

import core.builtins.custom_tags as ct


class TestCustomTags(TestCase):
    def test_highlight_text(self):
        span = '<mark class="lite-highlight">'
        span_end = "</mark>"
        actual_string = ct.highlight_text("this is a sassy string", "a")
        expected_string = "this is " + span + "a" + span_end + " s" + span + "a" + span_end + "ssy string"

        self.assertEqual(actual_string, expected_string)

    def test_strip_underscores(self):
        expected_value = "A long string"
        actual_value = ct.strip_underscores("a_long_string")

        self.assertEqual(actual_value, expected_value)

    def test_units_pluralise(self):
        expected_value = "grams"
        actual_value = ct.units_pluralise("gram(s)", "2")

        self.assertEqual(actual_value, expected_value)

    def test_units_dont_pluralise_with_one_unit(self):
        expected_value = "gram"
        actual_value = ct.units_pluralise("gram(s)", "1")

        self.assertEqual(actual_value, expected_value)

    def test_reference_code(self):
        expected_value = "12345-67890"
        actual_value = ct.reference_code("1234567890")

        self.assertEqual(actual_value, expected_value)

    def test_times(self):
        expected_value = [1, 2, 3, 4, 5]
        actual_value = ct.times(5)

        self.assertEqual(actual_value, expected_value)

    def test_default_na_with_value(self):
        expected_value = 1
        actual_value = ct.default_na(1)

        self.assertEqual(actual_value, expected_value)

    def test_default_na_without_value(self):
        expected_value = '<span class="lite-hint">N/A</span>'
        actual_value = ct.default_na(None)

        self.assertEqual(actual_value, expected_value)

    def test_friendly_boolean_true(self):
        expected_value = "Yes"
        actual_value = ct.friendly_boolean(True)

        self.assertEqual(actual_value, expected_value)

    def test_friendly_boolean_True(self):
        expected_value = "Yes"
        actual_value = ct.friendly_boolean("true")

        self.assertEqual(actual_value, expected_value)

    def test_friendly_boolean_anything_else(self):
        expected_value = "No"
        actual_value = ct.friendly_boolean("junk")

        self.assertEqual(actual_value, expected_value)

    def test_pluralise_unit_singular_with_s(self):
        expected_value = "gram"
        actual_value = ct.pluralise_unit("gram(s)", "1")

        self.assertEqual(actual_value, expected_value)

    def test_pluralise_unit_singular_without_s(self):
        expected_value = "gram"
        actual_value = ct.pluralise_unit("gram", "1")

        self.assertEqual(actual_value, expected_value)

    def test_pluralise_not_singular(self):
        expected_value = "number of objects"
        actual_value = ct.pluralise_unit("number of objects", "2")

        self.assertEqual(actual_value, expected_value)

    def test_str_date(self):
        expected_value = "4:56pm 23 December 1990"
        actual_value = ct.str_date("1990-12-23T16:56:19.000Z")

        self.assertEqual(actual_value, expected_value)

    def test_classname(self):
        expected_value = "type"
        actual_value = ct.classname(TestCase)

        self.assertEqual(actual_value, expected_value)
