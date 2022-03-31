import os
import requests

from dotenv import load_dotenv

load_dotenv("caseworker.env")

api_url = os.environ.get("LITE_API_URL")
vpn_user = os.getenv("VPN_USER")
vpn_password = os.getenv("VPN_PASSWORD")


def post(uri, kwargs):
    return requests.post(f"{api_url}/{uri}", auth=(vpn_user, vpn_password), **kwargs)


def put(uri, kwargs):
    return requests.put(f"{api_url}/{uri}", auth=(vpn_user, vpn_password), **kwargs)


def get(uri, kwargs):
    return requests.get(f"{api_url}/{uri}", auth=(vpn_user, vpn_password), **kwargs)
