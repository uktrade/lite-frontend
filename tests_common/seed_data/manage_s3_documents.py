from . import make_requests


def upload_test_document_to_aws(base_url):
    response = make_requests.make_request("GET", base_url=base_url, url='/static/upload-document-for-tests/',
                                          headers=None)

    if response.status_code == 200:
        return response.json()['s3_key']
    else:
        raise Exception(response.json()['errors'])
