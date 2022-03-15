import os
import re
from dotenv import load_dotenv


def set_sso_cookie(page):
    load_dotenv("caseworker.env")
    sso_url = os.environ.get("PW_SSO_URL")
    sso_user = os.environ.get("PW_SSO_USER")
    sso_pw = os.environ.get("PW_SSO_PASSWORD")

    getCsrfToken = page.request.get(sso_url)
    csrfToken = re.search("csrftoken=(.*); expires", getCsrfToken.headers["set-cookie"]).group(1)
    payload = {
        "username": sso_user,
        "password": sso_pw,
        "csrfmiddlewaretoken": csrfToken,
    }
    headers = {"referer": sso_url}
    page.request.post(sso_url, headers=headers, form=payload)
