from django.conf import settings
from notifications_python_client.notifications import NotificationsAPIClient
from requests.exceptions import RequestException


client = NotificationsAPIClient(settings.NOTIFY_KEY)


class NotifyException(Exception):
    pass


def send_feedback(feedback, user_email):
    try:
        client.send_email_notification(
            email_address=settings.NOTIFY_FEEDBACK_EMAIL,
            template_id=settings.NOTIFY_FEEDBACK_TEMPLATE_ID,
            personalisation={"feedback": feedback, "user_email": user_email},
        )
    except RequestException as e:
        raise NotifyException(f"Failed to email feedback: {str(e)}")
