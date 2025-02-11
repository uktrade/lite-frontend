from unittest import mock

from core.wizard.payloads import get_questions_data, get_cleaned_data


class TestGetQuestionsData:

    def test_get_questions_data_no_cleaned_data(self):
        form = mock.Mock()
        form.cleaned_data = None
        assert get_questions_data(form) == {}

    def test_get_questions_data_form_with_declared_fields(self):
        form = mock.Mock()
        form.cleaned_data.return_value = {"cleaned": "data"}
        mock_field = mock.Mock()
        mock_field.label = "Name"
        form.declared_fields = {
            "name": mock_field,
        }
        assert get_questions_data(form) == {"name": "Name"}


class TestGetCleanedData:

    def test_get_cleaned_data(self):
        form = mock.Mock()
        form.cleaned_data = {"some": "value"}
        assert get_cleaned_data(form) == {"some": "value"}
