from unittest import TestCase

from .helpers import nest_data, flatten_data


class FormTests(TestCase):

    def test_nest_data(self):
        value = {
            'reference': 'conversation_16',
            'organisation.name': 'Live on coffee and flowers inc.',
            'organisation.site.address.city': 'London',
            'organisation.site.name': 'Lemonworld',
            'user.first_name': "Matthew",
        }

        data = nest_data(value)

        self.assertEqual(data, {
            'reference': 'conversation_16',
            'organisation': {
                'name': 'Live on coffee and flowers inc.',
                'site': {
                    'address': {
                        'city': 'London',
                    },
                    'name': 'Lemonworld',
                }
            },
            'user': {
                'first_name': 'Matthew',
            }
        })

    def test_flatten_data(self):
        value = {
            'reference': 'conversation_16',
            'organisation': {
                'name': 'Live on coffee and flowers inc.',
                'site': {
                    'address': {
                        'city': 'London',
                    },
                    'name': 'Lemonworld',
                }
            },
            'user': {
                'first_name': 'Matthew',
            }
        }

        data = flatten_data(value)

        self.assertEqual(data, {
            'reference': 'conversation_16',
            'organisation.name': 'Live on coffee and flowers inc.',
            'organisation.site.address.city': 'London',
            'organisation.site.name': 'Lemonworld',
            'user.first_name': "Matthew",
        })
