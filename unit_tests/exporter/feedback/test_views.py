from unittest import mock

import pytest
from django.conf import settings
from django.urls import reverse
from requests.exceptions import RequestException
from requests.models import Response


@pytest.mark.parametrize("url", ("feedback", "thanks"))
def test_feedback_get_success(url, authorized_client):
    url = reverse(url)
    response = authorized_client.get(url)
    assert response.status_code == 200


@mock.patch("core.feedback.notify.client")
def test_feedback_post_success(mock_notify_client, authorized_client):
    # Set up response from notify
    notify_response = Response()
    notify_response.status_code = 200
    mock_notify_client.send_email_notification = mock.Mock(return_value=notify_response)
    # Hit with feedback
    url = reverse("feedback")
    response = authorized_client.post(url, data={"feedback": "test feedback"})
    assert response.status_code == 302
    assert response.url == reverse("thanks")
    mock_notify_client.send_email_notification.assert_called_once_with(
        email_address=settings.NOTIFY_FEEDBACK_EMAIL,
        template_id=settings.NOTIFY_FEEDBACK_TEMPLATE_ID,
        personalisation={"feedback": "test feedback", "user_email": authorized_client.session.get("email")},
    )


@mock.patch("core.feedback.notify.client")
def test_feedback_post_failure(mock_notify_client, authorized_client, caplog):
    # Set up response from notify
    notify_response = mock.Mock()
    exc = RequestException("test")
    mock_notify_client.send_email_notification = mock.Mock(side_effect=exc)
    # Hit with feedback
    url = reverse("feedback")
    response = authorized_client.post(url, data={"feedback": "test feedback"})
    assert response.status_code == 302
    assert response.url == reverse("thanks")
    mock_notify_client.send_email_notification.assert_called_once_with(
        email_address=settings.NOTIFY_FEEDBACK_EMAIL,
        template_id=settings.NOTIFY_FEEDBACK_TEMPLATE_ID,
        personalisation={"feedback": "test feedback", "user_email": authorized_client.session.get("email")},
    )
    assert "Failed to email feedback" in caplog.text
