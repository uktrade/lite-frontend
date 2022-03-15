import os
import requests

from dotenv import load_dotenv

load_dotenv("caseworker.env")

api_url = os.environ.get("PW_API_URL")


def post(uri, kwargs):
    return requests.post(f"{api_url}{uri}", **kwargs)


def put(uri, kwargs):
    return requests.put(f"{api_url}{uri}", **kwargs)


def get(uri, kwargs):
    return requests.get(f"{api_url}{uri}", **kwargs)
