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

def get_data_from_request(method, base_url, url, key, headers, body=None, files=None):
    return make_request(method, base_url, url, headers, body, files).json()[key]
