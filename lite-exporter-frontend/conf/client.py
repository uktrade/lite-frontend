import requests

from conf.settings import env


def get(request, appended_address):
    if request:
        return requests.get(
            env("LITE_API_URL") + appended_address,
            headers={
                "EXPORTER-USER-TOKEN": str(request.user.user_token),
                "X-Correlation-Id": str(request.correlation),
                "ORGANISATION-ID": str(request.user.organisation),
            },
        )

    return requests.get(env("LITE_API_URL") + appended_address)


def post(request, appended_address, json):
    return requests.post(
        env("LITE_API_URL") + appended_address,
        json=json,
        headers={
            "EXPORTER-USER-TOKEN": str(request.user.user_token),
            "X-Correlation-Id": str(request.correlation),
            "ORGANISATION-ID": str(request.user.organisation),
        },
    )


def put(request, appended_address: str, json):
    if not appended_address.endswith("/"):
        appended_address = appended_address + "/"

    return requests.put(
        env("LITE_API_URL") + appended_address,
        json=json,
        headers={
            "EXPORTER-USER-TOKEN": str(request.user.user_token),
            "X-Correlation-Id": str(request.correlation),
            "ORGANISATION-ID": str(request.user.organisation),
        },
    )


def delete(request, appended_address):
    return requests.delete(
        env("LITE_API_URL") + appended_address,
        headers={
            "EXPORTER-USER-TOKEN": str(request.user.user_token),
            "X-Correlation-Id": str(request.correlation),
            "ORGANISATION-ID": str(request.user.organisation),
        },
    )
