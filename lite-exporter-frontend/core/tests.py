from django.test import TestCase

from core.helpers import convert_parameters_to_query_params


class TestHelpers(TestCase):
    def test_convert_parameters_to_query_params(self):
        params = {
            'request': 'request',
            'org_type': ['individual', 'commercial'],
            'page': 1,
            'empty': None
        }

        self.assertEqual(convert_parameters_to_query_params(params), '?org_type=individual&org_type=commercial&page=1')
