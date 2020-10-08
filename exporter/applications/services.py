from http import HTTPStatus

from s3chunkuploader.file_handler import s3_client

from django.http import StreamingHttpResponse
from django.conf import settings

from core import client
from exporter.applications.helpers.date_fields import format_date_fields, create_formatted_date_from_components
from exporter.core.helpers import remove_prefix, add_validate_only_to_data
from core.helpers import convert_parameters_to_query_params
from exporter.core.objects import Application


def get_applications(request, page: int = 1, submitted: bool = True):
    """
    Returns a list of applications
    :param request: Standard HttpRequest object
    :param page: Returns n page of page results
    :param submitted: Returns submitted applications if True, else returns draft applications if False
    """
    querystring = convert_parameters_to_query_params({"page": page, "submitted": submitted})
    data = client.get(request, f"/applications/{querystring}")
    return data.json()


def has_existing_applications_and_licences_and_nlrs(request):
    """
    Returns if an hmrc org has any submitted queries
    Returns if a standard org has any applications & licences
    """
    data = client.get(request, "/applications/existing/")
    return data.json()


def get_application(request, pk) -> Application:
    response = client.get(request, f"/applications/{pk}")
    response.raise_for_status()
    return Application(response.json())


def post_applications(request, json):
    data = client.post(request, "/applications/", json)
    return data.json(), data.status_code


def put_application(request, pk, json):
    data = client.put(request, f"/applications/{pk}", json)
    return data.json(), data.status_code


def put_application_route_of_goods(request, pk, json):
    data = client.put(request, f"/applications/{pk}/route-of-goods/", json)
    return data.json(), data.status_code


def put_end_use_details(request, pk, json):
    data = client.put(request, f"/applications/{pk}/end-use-details/", json)
    return data.json(), data.status_code


def post_open_general_licences_applications(_, json):
    # Placeholder for LT-2110
    return json, 200


def put_temporary_export_details(request, pk, json):
    if "year" in json and "month" in json and "day" in json:
        json["proposed_return_date"] = create_formatted_date_from_components(json)

    data = client.put(request, f"/applications/{pk}/temporary-export-details/", json)
    return data.json(), data.status_code


def put_application_with_clearance_types(request, pk, json):
    # Inject the clearance types as an empty set into JSON if they are not present
    json["types"] = json.get("types", [])
    data = client.put(request, f"/applications/{pk}", json)
    return data.json(), data.status_code


def delete_application(request, pk):
    data = client.delete(request, f"/applications/{pk}")
    return data.json(), data.status_code


def submit_application(request, pk, json=None):
    json = json or {}
    data = client.put(request, f"/applications/{pk}/submit/", data=json)
    return data.json(), data.status_code


def get_application_goods(request, pk):
    data = client.get(request, f"/applications/{pk}/goods/")
    return data.json().get("goods") if data.status_code == HTTPStatus.OK else None


def validate_application_good(request, pk, json):
    post_data = get_data_from_post_good_on_app(json)
    post_data["validate_only"] = True
    return client.post(request, f"/applications/{pk}/goods/", post_data)


def get_application_goods_types(request, pk):
    data = client.get(request, f"/applications/{pk}/goodstypes/")
    return data.json().get("goods") if data.status_code == HTTPStatus.OK else None


def post_good_on_application(request, pk, json):
    post_data = get_data_from_post_good_on_app(json)
    if "good_id" not in post_data:
        post_data["good_id"] = json["good_id"]
    data = client.post(request, f"/applications/{pk}/goods/", post_data)
    return data.json(), data.status_code


def get_data_from_post_good_on_app(json):
    if json.get("good_on_app_value") or json.get("good_on_app_value") == "":
        post_data = remove_prefix(json, "good_on_app_")
    else:
        post_data = json
    return post_data


def get_application_countries(request, pk):
    data = client.get(request, f"/applications/{pk}/countries/")
    return [country_entry["country"] for country_entry in data.json()["countries"]]


def get_application_countries_and_contract_types(request, pk):
    data = client.get(request, f"/applications/{pk}/countries-contract-types/")
    return data.json()


def post_application_countries(request, pk, json):
    data = client.post(request, f"/applications/{pk}/countries/", json)
    return data.json(), data.status_code


def put_contract_type_for_country(request, pk, json):
    data = client.put(request, f"/applications/{pk}/contract-types/", json)
    return data.json(), data.status_code


def validate_party(request, pk, json):
    json = add_validate_only_to_data(json)
    data = client.post(request, f"/applications/{pk}/parties/", json)
    return data.json(), data.status_code


def post_party(request, pk, json):
    data = client.post(request, f"/applications/{pk}/parties/", json)
    return data.json(), data.status_code


def copy_party(request, pk, party_pk):
    return client.get(request, f"/applications/{pk}/parties/{party_pk}/copy/").json()["party"]


def delete_party(request, application_pk, obj_pk=None):
    return client.delete(request, f"/applications/{application_pk}/parties/{obj_pk}/").status_code


def get_party(request, application_pk, pk):
    return client.get(request, f"/applications/{application_pk}/parties/{pk}/").json()


def delete_party_document(request, application_pk, obj_pk):
    data = client.delete(request, f"/applications/{application_pk}/parties/{obj_pk}/document/")
    return data.status_code


def post_party_document(request, application_pk, obj_pk, json):
    data = client.post(request, f"/applications/{application_pk}/parties/{obj_pk}/document/", data=json)
    return data.json(), data.status_code


def get_party_document(request, application_pk, obj_pk):
    data = client.get(request, f"/applications/{application_pk}/parties/{obj_pk}/document/")
    return data.json(), data.status_code


def get_ultimate_end_users(request, pk):
    data = client.get(request, f"/applications/{pk}/parties/?type=ultimate_end_user")
    return data.json()["ultimate_end_users"]


def get_third_parties(request, pk):
    data = client.get(request, f"/applications/{pk}/parties/?type=third_party")
    return data.json()["third_parties"]


def get_existing_parties(request, pk, name=None, address=None, country=None, party_type=None, page=1):
    params = {"name": name, "address": address, "country": country, "party_type": party_type, "page": page}
    params = convert_parameters_to_query_params(params)
    data = client.get(request, f"/applications/{pk}/existing-parties/{params}")
    return data.json(), data.status_code


def post_additional_document(request, pk, json):
    data = client.post(request, f"/applications/{pk}/documents/", json)
    return data.json(), data.status_code


def get_additional_documents(request, pk):
    data = client.get(request, f"/applications/{pk}/documents/")
    return data.json(), data.status_code


def get_additional_document(request, pk, doc_pk):
    data = client.get(request, f"/applications/{pk}/documents/{doc_pk}/")
    return data.json(), data.status_code


def delete_additional_party_document(request, pk, doc_pk):
    data = client.delete(request, f"/applications/{pk}/documents/{doc_pk}/")
    return data.status_code


def delete_application_preexisting_good(request, good_on_application_pk):
    response = client.delete(request, f"/applications/good-on-application/{good_on_application_pk}")
    return response.status_code


def get_case_notes(request, pk):
    data = client.get(request, f"/cases/{pk}/case-notes/")
    return data.json()


def post_case_notes(request, pk, json):
    data = client.post(request, f"/cases/{pk}/case-notes/", json)
    return data.json(), data.status_code


def get_application_ecju_queries(request, pk):
    data = client.get(request, f"/cases/{pk}/ecju-queries/").json()["ecju_queries"]

    open_queries = [x for x in data if not x["response"]]
    closed_queries = [x for x in data if x["response"]]

    return open_queries, closed_queries


def get_case_generated_documents(request, pk):
    data = client.get(request, f"/cases/{pk}/generated-documents/")
    return data.json(), data.status_code


def get_status_properties(request, status):
    data = client.get(request, "/static/statuses/properties/" + status)
    return data.json(), data.status_code


def set_application_status(request, pk, status):
    json = {"status": status}
    data = client.put(request, f"/applications/{pk}/status/", json)
    return data.json(), data.status_code


def add_document_data(request):
    files = request.FILES.getlist("file")
    if not files:
        return None, "No files attached"
    if len(files) != 1:
        return None, "Multiple files attached"
    file = files[0]
    try:
        original_name = file.original_name
    except Exception:  # noqa
        original_name = file.name

    data = {
        "name": original_name,
        "s3_key": file.name,
        "size": int(file.size // 1024) if file.size else 0,  # in kilobytes
    }
    if "description" in request.POST:
        data["description"] = request.POST.get("description")

    return data, None


def generate_file(result):
    for chunk in iter(lambda: result["Body"].read(settings.STREAMING_CHUNK_SIZE), b""):
        yield chunk


def download_document_from_s3(s3_key, original_file_name):
    s3 = s3_client()
    s3_response = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    _kwargs = {}
    if s3_response.get("ContentType"):
        _kwargs["content_type"] = s3_response["ContentType"]
    response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
    response["Content-Disposition"] = f'attachment; filename="{original_file_name}"'
    return response


def get_goods_type(request, app_pk, good_pk):
    data = client.get(request, f"/applications/{app_pk}/goodstype/{good_pk}/")
    return data.json(), data.status_code


def post_goods_type(request, app_pk, json):
    data = client.post(request, f"/applications/{app_pk}/goodstypes/", json)
    return data.json(), data.status_code


def delete_goods_type(request, app_pk, good_pk):
    data = client.delete(request, f"/applications/{app_pk}/goodstype/" + good_pk + "/")
    return data.status_code


def put_goods_type_countries(request, app_pk, json):
    data = client.put(request, f"/applications/{app_pk}/goodstype/assign-countries/", json)
    return data.json(), data.status_code


def get_goods_type_document(request, pk, good_pk):
    data = client.get(request, f"/applications/{pk}/goodstype/{good_pk}/document/")
    return data.json(), data.status_code


def post_goods_type_document(request, pk, good_pk, json):
    data = client.post(request, f"/applications/{pk}/goodstype/{good_pk}/document/", json)
    return data.json(), data.status_code


def delete_goods_type_document(request, pk, good_pk):
    data = client.delete(request, f"/applications/{pk}/goodstype/{good_pk}/document/")
    return data.status_code


def get_activity(request, pk):
    data = client.get(request, f"/applications/{pk}/activity/")
    return data.json()["activity"]


def copy_application(request, pk, data):
    data = client.post(request, f"/applications/{pk}/copy/", data=data)
    return data.json(), data.status_code


def post_exhibition(request, pk, data):
    post_data = format_date_fields(data)
    data = client.post(request, f"/applications/{pk}/exhibition-details/", data=post_data)
    return data.json(), data.status_code
