from unittest import TestCase

from lite_forms.components import Form, DetailComponent, TextInput
from lite_forms.helpers import nest_data, flatten_data, remove_unused_errors, get_form_by_pk


class FormTests(TestCase):

    def test_get_form_by_pk(self):
        forms = [Form(pk=123, questions=[]), Form(questions=[]), Form(questions=[])]

        self.assertEqual(str(get_form_by_pk('123', forms).pk), '123')

    def test_remove_unused_errors(self):
        form = Form(questions=[
            TextInput('name'),
            TextInput('age'),
            TextInput('password'),
            DetailComponent('', ''),
        ])

        errors = {
            'name': 'This field must not be empty',
            'email': 'This field must not be empty',
            'age': 'This field must not be empty',
            'password': 'This field must not be empty',
        }

        cleaned_errors = {
            'name': 'This field must not be empty',
            'age': 'This field must not be empty',
            'password': 'This field must not be empty',
        }

        self.assertEqual(cleaned_errors, remove_unused_errors(errors, form))

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
