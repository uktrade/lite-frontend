from unittest import TestCase

from cases.helpers.advice import order_grouped_advice, convert_advice_item_to_base64


class CaseTests(TestCase):
    def test_convert_advice_item_to_base64(self):
        """
        Asserts that advice comparison is case and space insensitive
        """
        item_1 = {
            "text": "I Am Easy to Find",
            "note": "I Am Easy to Find",
            "type": "I Am Easy to Find",
            "level": "I Am Easy to Find",
        }
        item_2 = {
            "text": "Iameasytofind",
            "note": "I Am Easy to Find",
            "type": "I Am Easy to Find",
            "level": "I Am Easy to Find",
        }
        self.assertEqual(convert_advice_item_to_base64(item_1), convert_advice_item_to_base64(item_2))

    def test_order_grouped_advice(self):
        """
        Asserts ordering of conflicting, approve, proviso, no_licence_required,
        not_applicable, refuse, no_advice
        """
        initial_order = {
            1: {"type": {"key": "refuse"}},
            2: {"type": {"key": "approve"}},
            3: {"type": {"key": "no_licence_required"}},
            4: {"type": {"key": "refuse"}},
            5: {"type": {"key": "conflicting"}},
            6: {"type": {"key": "no_advice"}},
            7: {"type": {"key": "not_applicable"}},
        }

        ordered = list(order_grouped_advice(initial_order).keys())

        self.assertEqual(ordered[0], 5)
        self.assertEqual(ordered[1], 2)
        self.assertEqual(ordered[2], 3)
        self.assertEqual(ordered[3], 7)
        self.assertEqual(ordered[4], 1)
        self.assertEqual(ordered[5], 4)
        self.assertEqual(ordered[6], 6)
