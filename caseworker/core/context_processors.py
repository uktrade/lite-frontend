from django.conf import settings
from django.urls import reverse_lazy


from caseworker.core.constants import Permission, Role
from caseworker.core.services import (
    get_user_permissions,
    get_menu_notifications,
    get_new_mention_count,
    get_user_role_name,
)
from lite_content.lite_internal_frontend import strings, open_general_licences
from lite_content.lite_internal_frontend.flags import FlagsList
from lite_content.lite_internal_frontend.organisations import OrganisationsPage
from lite_content.lite_internal_frontend.queues import QueuesList
from lite_content.lite_internal_frontend.teams import TeamsPage
from lite_content.lite_internal_frontend.users import UsersPage
from lite_forms.helpers import conditional
from caseworker.queues.services import get_queue
from caseworker.users.services import get_gov_user
from caseworker.core.constants import ALL_CASES_QUEUE_ID


def current_queue_and_user(request):
    extra_context = {}
    kwargs = getattr(request.resolver_match, "kwargs", {})
    queue = None
    if "queue_pk" in kwargs and "disable_queue_lookup" not in kwargs:
        queue_pk = request.resolver_match.kwargs["queue_pk"]
        queue = get_queue(request, queue_pk)
    extra_context["queue"] = queue

    current_user = None
    if "lite_api_user_id" in request.session:
        user, _ = get_gov_user(request, str(request.session["lite_api_user_id"]))
        current_user = user.get("user", None)
    extra_context["current_user"] = current_user

    return extra_context


def export_vars(request):
    return {
        "GTM_ID": settings.GTM_ID,
        "CURRENT_PATH": request.get_full_path(),
        "CURRENT_PATH_WITHOUT_PARAMS": request.get_full_path().split("?")[0].split("#")[0],
        "CURRENT_PATH_ONLY_PARAMS": (
            "?" + request.get_full_path().split("?")[1] if "?" in request.get_full_path() else ""
        ),
    }


def lite_menu(request):
    has_notifications = False
    if "lite_api_user_id" in request.session:
        permissions = get_user_permissions(request)
        role_name = get_user_role_name(request)
        notifications = get_menu_notifications(request)
        notification_data = notifications["notifications"]
        has_notifications = notifications["has_notifications"]
        queue_pk = request.session["default_queue"]
        pages = [
            {
                "title": "Cases",
                "url": reverse_lazy("queues:cases", kwargs={"queue_pk": queue_pk}),
                "icon": "menu/cases",
            },
            {
                "title": OrganisationsPage.TITLE,
                "url": reverse_lazy("organisations:organisations"),
                "icon": "menu/businesses",
                "notifications": notification_data.get("organisations"),
            },
            {"title": TeamsPage.TITLE, "url": reverse_lazy("teams:teams"), "icon": "menu/teams"},
            {"title": "My Team", "url": reverse_lazy("teams:team"), "icon": "menu/teams"},
            {"title": QueuesList.TITLE, "url": reverse_lazy("queues:manage"), "icon": "menu/queues"},
            {"title": UsersPage.TITLE, "url": reverse_lazy("users:users"), "icon": "menu/users"},
            {"title": FlagsList.TITLE, "url": reverse_lazy("flags:flags"), "icon": "menu/flags"},
            conditional(
                Permission.MAINTAIN_OGL.value in permissions,
                {
                    "title": open_general_licences.List.TITLE,
                    "url": reverse_lazy("open_general_licences:open_general_licences"),
                    "icon": "menu/open-general-licences",
                },
            ),
            conditional(
                Permission.CONFIGURE_TEMPLATES.value in permissions,
                {
                    "title": strings.DOCUMENT_TEMPLATES_TITLE,
                    "url": reverse_lazy("letter_templates:letter_templates"),
                    "icon": "menu/letter-templates",
                },
            ),
            conditional(
                Permission.MANAGE_FLAGGING_RULES.value in permissions,
                {"title": "Flagging rules", "url": reverse_lazy("flags:flagging_rules"), "icon": "menu/flags"},
            ),
            conditional(
                Permission.MANAGE_TEAM_ROUTING_RULES.value in permissions
                or Permission.MANAGE_ALL_ROUTING_RULES.value in permissions,
                {"title": "Routing rules", "url": reverse_lazy("routing_rules:list"), "icon": "menu/routing-rules"},
            ),
            conditional(
                role_name in Role.tau_roles.value,
                {"title": "Denial records", "url": reverse_lazy("external_data:denials-upload"), "icon": "menu/cases"},
            ),
        ]
    else:
        pages = []
    return {
        "LITE_MENU": [x for x in pages if x is not None],
        "MENU_NOTIFICATIONS": has_notifications,
    }


def new_mentions(request):
    new_mentions = 0
    if "lite_api_user_id" in request.session:
        results, _ = get_new_mention_count(request)
        new_mentions = results["count"]
    return {
        "NEW_MENTIONS_COUNT": new_mentions,
    }


def all_cases_queue(request):
    kwargs = getattr(request.resolver_match, "kwargs", {})
    is_all_cases_queue = False
    if "queue_pk" in kwargs:
        queue_pk = request.resolver_match.kwargs["queue_pk"]
        is_all_cases_queue = str(queue_pk) == ALL_CASES_QUEUE_ID
    return {
        "is_all_cases_queue": is_all_cases_queue,
        "all_cases_queue_id": ALL_CASES_QUEUE_ID,
    }


def feature_flags(request):
    return {}
