import requests


def make_request(self, method, url, headers=None, body=None, files=None):
    if headers is None:
        headers = self.gov_headers
    if body:
        response = requests.request(method, self.base_url + url,
                                    json=body,
                                    headers=headers,
                                    files=files)
    else:
        response = requests.request(method, self.base_url + url, headers=headers)
    if not response.ok:
        raise Exception('bad response: ' + response.text)
    return response