from django.test import TestCase

from applications.libraries.reverse_documents import document_switch


class TestHelpers(TestCase):

    def test_document_switch(self):
        self.assertEqual(len(document_switch('ultimate-end-user')), 6)
        self.assertEqual(len(document_switch('end-user')), 6)
        self.assertEqual(len(document_switch('consignee')), 6)
        self.assertEqual(len(document_switch('goods-type')), 6)
        self.assertEqual(len(document_switch('additional-document')), 6)

        with self.assertRaises(NotImplementedError):
            document_switch('does-not-support-this')
