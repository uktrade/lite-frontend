import requests


def make_request(method, base_url, url, headers, body=None, files=None):
    if body:
        response = requests.request(method, base_url + url,
                                    json=body,
                                    headers=headers,
                                    files=files)
    else:
        response = requests.request(method, base_url + url, headers=headers)
    if not response.ok:
        raise Exception('bad response: ' + response.text)
    return response
