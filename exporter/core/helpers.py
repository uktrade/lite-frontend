import datetime

from dateutil.parser import parse
from html import escape
from typing import List

from django.conf import settings
from django.template.defaultfilters import safe
from django.templatetags.tz import localtime
from django.utils.safestring import mark_safe

from exporter.core import decorators
from exporter.core import constants
from exporter.core.constants import AddGoodFormSteps, SetPartyFormSteps
from core.builtins.custom_tags import default_na
from exporter.organisation.roles.services import get_user_permissions


class Section:
    def __init__(self, title, tiles):
        self.title = title
        self.tiles = tiles


class Tile:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url


def str_to_bool(v, invert_none=False):
    if v is None:
        return invert_none
    if isinstance(v, bool):
        return v
    return v.lower() in ("yes", "true", "t", "1")


def str_date_only(value):
    return localtime(parse(value)).strftime("%d %B %Y")


def generate_notification_string(notifications, case_types):
    notification_count = notifications["notifications"]
    notification_count_sum = sum([count for case_type, count in notification_count.items() if case_type in case_types])
    return generate_notification_total_string(notification_count_sum)


def generate_notification_total_string(notification_count):
    if not notification_count:
        return ""
    elif notification_count == 1:
        return f"You have {notification_count} new notification"
    else:
        return f"You have {notification_count} new notifications"


def convert_to_link(address, name=None, classes="", include_br=False):
    """
    Returns a correctly formatted, safe link to an address
    Returns default_na if no address is provided
    """
    if not address:
        return default_na(None)

    if not name:
        name = address

    address = escape(address)
    name = escape(name)

    br = "<br>" if include_br else ""

    return safe(f'<a href="{address}" class="govuk-link govuk-link--no-visited-state {classes}">{name}</a>{br}')


def remove_prefix(json, prefix):
    post_data = {}
    for k in json:
        if k.startswith(prefix):
            field = k[len(prefix) :]
            post_data[field] = json[k]
    return post_data


def has_permission(request, permission):
    """
    Returns true if the user has a given permission, else false
    """
    user_permissions = get_user_permissions(request)
    return permission in user_permissions, user_permissions


def decorate_patterns_with_permission(patterns, permission, ignore: List[str] = None):
    def _wrap_with_permission(_permission, view_func=None):
        actual_decorator = decorators.has_permission(_permission)

        if view_func:
            return actual_decorator(view_func)
        return actual_decorator

    if ignore is None:
        ignore = []

    decorated_patterns = []
    for pattern in patterns:
        callback = pattern.callback
        if pattern.name in ignore:
            continue
        pattern.callback = _wrap_with_permission(permission, callback)
        pattern._callback = _wrap_with_permission(permission, callback)
        decorated_patterns.append(pattern)
    return decorated_patterns


def add_validate_only_to_data(data):
    data = data.copy()
    data["validate_only"] = True

    return data


def convert_control_list_entries(control_list_entries):
    return default_na(
        mark_safe(  # nosec
            ", ".join(
                [
                    "<span data-definition-title='"
                    + clc["rating"]
                    + "' data-definition-text='"
                    + clc.get("text", "")
                    + "'>"
                    + clc["rating"]
                    + "</span>"
                    for clc in control_list_entries
                ]
            )
        )
    )


def get_firearms_subcategory(type):
    is_firearm = type == constants.FIREARMS
    is_firearm_ammunition_or_component = type in constants.FIREARM_AMMUNITION_COMPONENT_TYPES
    is_firearms_accessory = type == constants.FIREARMS_ACCESSORY
    is_firearms_software_or_tech = type in constants.FIREARMS_SOFTWARE_TECH
    return is_firearm, is_firearm_ammunition_or_component, is_firearms_accessory, is_firearms_software_or_tech


def is_category_firearms(wizard):
    product_category_cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFormSteps.PRODUCT_CATEGORY)
    if not product_category_cleaned_data:
        return True

    item_category = product_category_cleaned_data["item_category"]
    return item_category == constants.PRODUCT_CATEGORY_FIREARM or settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS


def is_product_type(product_type):
    def _is_product_type(wizard):
        type_ = wizard.get_product_type()

        if not type_:
            return True

        (
            is_firearm,
            is_ammunition_or_component,
            is_firearms_accessory,
            is_firearms_software_or_tech,
        ) = get_firearms_subcategory(type_)

        return {
            "firearm": is_firearm,
            "ammunition_or_component": is_ammunition_or_component,
            "firearms_accessory": is_firearms_accessory,
            "firearms_software_or_tech": is_firearms_software_or_tech,
        }[product_type]

    return _is_product_type


def is_draft(wizard):
    try:
        return bool(str(wizard.kwargs["pk"]))
    except KeyError:
        return False


def is_pv_graded(wizard):
    add_goods_cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFormSteps.ADD_GOODS_QUESTIONS)

    return str_to_bool(add_goods_cleaned_data.get("is_pv_graded"))


def show_serial_numbers_form(indentification_markings_step_name):
    def _show_serial_numbers_form(wizard):
        cleaned_data = wizard.get_cleaned_data_for_step(indentification_markings_step_name)
        return cleaned_data.get("serial_numbers_available") == "AVAILABLE"

    return _show_serial_numbers_form


def is_preexisting(default):
    def _is_preexisting(wizard):
        return str_to_bool(wizard.request.GET.get("preexisting", default))

    return _is_preexisting


def show_rfd_form(wizard):
    preexisting = is_preexisting(False)(wizard)

    try:
        application = wizard.application
    except AttributeError:
        application = {}

    if preexisting:
        return is_product_type("ammunition_or_component")(wizard) and has_expired_rfd_certificate(application)

    return is_product_type("ammunition_or_component")(wizard) and not has_valid_rfd_certificate(application)


def show_attach_rfd_form(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(AddGoodFormSteps.REGISTERED_FIREARMS_DEALER)

    return str_to_bool(cleaned_data.get("is_registered_firearm_dealer"))


def has_expired_rfd_certificate(application):
    document = get_rfd_certificate(application)
    return bool(document) and document["is_expired"]


def has_valid_rfd_certificate(application):
    document = get_rfd_certificate(application)
    return bool(document) and not document["is_expired"]


def get_organisation_documents(application):
    return {item["document_type"]: item for item in application.get("organisation", {}).get("documents", [])}


def get_rfd_certificate(application):
    documents = get_organisation_documents(application)
    return documents.get(constants.DocumentType.RFD_CERTIFICATE)


def is_end_user_document_available(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(SetPartyFormSteps.PARTY_DOCUMENTS)
    return str_to_bool(cleaned_data.get("end_user_document_available"))


def is_document_in_english(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD)
    return str_to_bool(cleaned_data.get("document_in_english"))


def is_document_on_letterhead(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step(SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD)
    return str_to_bool(cleaned_data.get("document_on_letterhead"))


def decompose_date(field_name, date):
    return {
        f"{field_name}_0": date.day,
        f"{field_name}_1": date.month,
        f"{field_name}_2": date.year,
    }


def get_document_data(file):
    return {
        "name": getattr(file, "original_name", file.name),
        "s3_key": file.name,
        "size": int(file.size // 1024) if file.size else 0,  # in kilobytes
    }


def has_firearm_act_document(application, document_type):
    documents = get_organisation_documents(application)
    return document_type in documents


def get_firearm_act_document(application, document_type):
    documents = get_organisation_documents(application)
    return documents[document_type]


def convert_api_date_string_to_date(date_str):
    return datetime.datetime.strptime(date_str, "%d %B %Y").date()
