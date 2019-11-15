from unittest import TestCase

from queues.helpers import get_assigned_users_from_cases, add_assigned_users_to_cases


class QueuesTests(TestCase):
    def test_get_assigned_users_from_cases(self):
        case_ids = ["adb55711-7fd4-43e1-8e3c-eef84057a846"]
        case_assignments = [
            {
                "case": "adb55711-7fd4-43e1-8e3c-eef84057a846",
                "users": [
                    {
                        "id": "1rylan-1102-441f-a7b4-d55e83989b3b",
                        "first_name": "Matt",
                        "last_name": "Berninger",
                        "email": "matt.berninger@mail.com",
                    }
                ],
            },
            {
                "case": "completely-random-case-id-that-we-dont-want!",
                "users": [
                    {
                        "id": "373e0d9c-1102-441f-a7b4-123234235345",
                        "first_name": "Aaron",
                        "last_name": "Dessner",
                        "email": "aaron.dessner@mail.com",
                    }
                ],
            },
        ]
        correct_outcome = [
            {
                "id": "1rylan-1102-441f-a7b4-d55e83989b3b",
                "first_name": "Matt",
                "last_name": "Berninger",
                "email": "matt.berninger@mail.com",
            }
        ]

        self.assertEqual(correct_outcome, get_assigned_users_from_cases(case_ids, case_assignments))

    def tests_add_assigned_users_to_cases(self):
        case_ids = [
            {"id": "adb55711-7fd4-43e1-8e3c-eef84057a846"},
            {"id": "12355711-7fd4-43e1-8e3c-eef84057a846"},
            {"id": "45655711-7fd4-43e1-8e3c-eef84057a846"},
        ]
        case_assignments = [
            {
                "case": "adb55711-7fd4-43e1-8e3c-eef84057a846",
                "users": [
                    {
                        "id": "1rylan-1102-441f-a7b4-d55e83989b3b",
                        "first_name": "Matt",
                        "last_name": "Berninger",
                        "email": "matt.berninger@mail.com",
                    }
                ],
            },
            {
                "case": "12355711-7fd4-43e1-8e3c-eef84057a846",
                "users": [
                    {
                        "id": "373e0d9c-1102-441f-a7b4-123234235345",
                        "first_name": "Aaron",
                        "last_name": "Dessner",
                        "email": "aaron.dessner@mail.com",
                    }
                ],
            },
        ]
        correct_outcome = [
            {
                "id": "adb55711-7fd4-43e1-8e3c-eef84057a846",
                "assignments": [
                    {
                        "id": "1rylan-1102-441f-a7b4-d55e83989b3b",
                        "first_name": "Matt",
                        "last_name": "Berninger",
                        "email": "matt.berninger@mail.com",
                    }
                ],
            },
            {
                "id": "12355711-7fd4-43e1-8e3c-eef84057a846",
                "assignments": [
                    {
                        "id": "373e0d9c-1102-441f-a7b4-123234235345",
                        "first_name": "Aaron",
                        "last_name": "Dessner",
                        "email": "aaron.dessner@mail.com",
                    }
                ],
            },
            {"id": "45655711-7fd4-43e1-8e3c-eef84057a846"},
        ]

        self.assertEqual(correct_outcome, add_assigned_users_to_cases(case_ids, case_assignments))
