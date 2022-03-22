from django.shortcuts import render

from exporter.applications.constants import OielLicenceTypes
from exporter.applications.helpers.check_your_answers import (
    _is_application_export_type_temporary,
    get_application_type_string,
)
from exporter.applications.helpers.parties import party_requires_ec3_document
from exporter.applications.helpers.task_list_sections import (
    get_reference_number_description,
    get_edit_type,
    get_route_of_goods,
    get_temporary_export_details,
    get_product_location_and_journey_details,
)
from exporter.applications.services import (
    get_application_goods,
    get_additional_documents,
    get_application_countries_and_contract_types,
    get_case_notes,
)
from exporter.core.constants import (
    HMRC,
    OPEN,
    STANDARD,
    EXHIBITION,
    F680,
    GIFTING,
    PartyDocumentType,
    Permissions,
    CaseTypes,
)
from core.constants import GoodsTypeCategory
from lite_content.lite_exporter_frontend.strings import applications
from exporter.organisation.roles.services import get_user_permissions


def _get_strings(application_type):
    if application_type == STANDARD:
        return applications.StandardApplicationTaskList
    elif application_type == OPEN:
        return applications.OpenApplicationTaskList
    elif application_type == HMRC:
        return applications.HMRCApplicationTaskList
    elif application_type == EXHIBITION:
        return applications.ExhibitionClearanceTaskList
    elif application_type == F680:
        return applications.F680ClearanceTaskList
    elif application_type == GIFTING:
        return applications.GiftingClearanceTaskList
    elif application_type == HMRC:
        return applications.HMRCApplicationTaskList
    else:
        raise NotImplementedError(f"No string class for given for {application_type}")


def get_application_task_list(request, application, errors=None):
    user_permissions = get_user_permissions(request)
    additional_documents, _ = get_additional_documents(request, application["id"])
    application_type = application.sub_type
    is_editing, edit_type = get_edit_type(application)

    context = {
        "strings": _get_strings(application_type),
        "application": application,
        "application_type": application_type,
        "is_editing": is_editing,
        "edit_type": edit_type,
        "licence_type": get_application_type_string(application),
        "errors": errors,
    }

    require_ec3 = party_requires_ec3_document(application)
    end_user = application.get("end_user", {})
    ec3_details_available = False
    if end_user:
        ec3_document_available = any(
            document["type"] == PartyDocumentType.END_USER_EC3_DOCUMENT for document in end_user["documents"]
        )
        ec3_details_available = ec3_document_available or end_user["ec3_missing_reason"]

    context["show_ec3_banner"] = require_ec3 and not ec3_details_available

    if application_type == HMRC:
        context["locations"] = application["goods_locations"] or application["have_goods_departed"]
        return render(request, "applications/hmrc-application.html", context)

    context["can_submit"] = Permissions.SUBMIT_LICENCE_APPLICATION in user_permissions
    context["supporting_documents"] = additional_documents["documents"]
    context["locations"] = get_product_location_and_journey_details(application)
    context["notes"] = get_case_notes(request, application["id"])["case_notes"]

    if application_type == STANDARD:
        context["reference_number_description"] = get_reference_number_description(application)
        context["route_of_goods"] = get_route_of_goods(application)
        if _is_application_export_type_temporary(application):
            context["temporary_export_details"] = get_temporary_export_details(application)
    elif application_type == OPEN:
        context["countries"] = [
            country_entry["country_id"]
            for country_entry in get_application_countries_and_contract_types(request, application["id"])["countries"]
        ]
        context["goodstypes"] = application["goods_types"]
        if _is_application_export_type_temporary(application):
            context["temporary_export_details"] = get_temporary_export_details(application)
        goods_types = application.get("goods_types")
        if goods_types:
            destination_countries = [goods_type["countries"] for goods_type in goods_types][0]
            context["destinations"] = set([destination["id"] for destination in destination_countries])
            if application["goodstype_category"]["key"] == GoodsTypeCategory.MILITARY:
                context["ultimate_end_users_required"] = True in [
                    goods_type["is_good_incorporated"] for goods_type in goods_types
                ]
        context["route_of_goods"] = get_route_of_goods(application)
        context["is_oicl_appplication"] = application.type_reference == CaseTypes.OICL
        if application.get("goodstype_category"):
            goodstype_category = application.get("goodstype_category").get("key")
            context["is_uk_continental_shelf_application"] = (
                goodstype_category == GoodsTypeCategory.UK_CONTINENTAL_SHELF
            )
            countries_and_contract_types = get_application_countries_and_contract_types(request, application["id"])[
                "countries"
            ]
            if context["is_uk_continental_shelf_application"]:
                context["countries_missing_contract_types"] = [
                    entry["country_id"] for entry in countries_and_contract_types if not entry["contract_types"]
                ]
            context["is_crypto_application"] = goodstype_category == GoodsTypeCategory.CRYPTOGRAPHIC
            context["is_military_dual_use_application"] = goodstype_category == GoodsTypeCategory.MILITARY
            context["oiel_noneditable_countries"] = OielLicenceTypes.is_non_editable_country(goodstype_category)

        # Check if contract types include 'nuclear_related' and set attribute end_user_mandatory
        contract_types = []
        for country in countries_and_contract_types:
            if country["contract_types"]:
                contract_types.extend(country["contract_types"].split(","))

        context["end_user_mandatory"] = "nuclear_related" in set(contract_types)

    if not application_type == OPEN:
        context["goods"] = get_application_goods(request, application["id"])
        context["ultimate_end_users_required"] = True in [good["is_good_incorporated"] for good in context["goods"]]

    return render(request, "applications/task-list.html", context)
