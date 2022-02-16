import astroid
from pylint.interfaces import IAstroidChecker
from pylint.checkers import BaseChecker


def node_isinstance(node, class_name):
    if not isinstance(node, astroid.ClassDef):
        return False

    return any(base.qname() == class_name for base in node.mro())


class OpenToAnonymousUsersChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = "login_required_checker"
    msgs = {
        "W1001": (
            "%s is open to anonymous users. Either use LoginRequiredMixin on the view or exclude it from this check",
            "open-to-anon",
            "Open to anonymous users",
        ),
    }
    options = (
        (
            "anonymous-users-allowed",
            {
                "default": [],
                "type": "csv",
                "metavar": "<csv>",
                "help": "Views that users can view without logging in",
            },
        ),
    )

    def visit_classdef(self, node):
        if node_isinstance(node, "django.views.generic.base.View") and not node_isinstance(
            node, "core.auth.views.LoginRequiredMixin"
        ):
            if node.qname() not in self.config.anonymous_users_allowed:
                self.add_message("W1001", node=node, args=(node.name,))


def register(linter):
    linter.register_checker(OpenToAnonymousUsersChecker(linter))
