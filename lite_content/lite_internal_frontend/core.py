from django.conf import settings


def get_human_readable_exception(status_code):
    """
    Returns friendly help text for exceptions (such as 400s, 403s, 404s and 500s)
    If a status code hasn't been handled here we'll just return the generic error text
    """
    support_text = f"Contact [support](mailto:{settings.LITE_FEEDBACK_EMAIL}) if you need any help."

    data = {
        404: {
            "title": "Page not found",
            "description": "If you entered a web address, check it is correct.\n\n\n\n"
            "If you pasted the web address, check you copied the entire address.\n\n\n\n"
            "You can browse from the [homepage](/) to find the information you need.\n\n\n\n" + support_text,
        },
        "generic": {
            "title": "Sorry, there is a problem with the service",
            "description": "Try again later.\n\n\n\n" + support_text,
        },
    }

    if status_code not in data:
        return data["generic"]

    return data[status_code]
