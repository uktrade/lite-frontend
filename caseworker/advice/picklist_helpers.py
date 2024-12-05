from caseworker.picklists.services import get_picklists_list


def approval_picklist(self):
    return {
        "approval_reason": get_picklists_list(
            self.request, type="standard_advice", disable_pagination=True, show_deactivated=False
        )
    }


def fcdo_picklist(self):
    return {
        "approval_reason": get_picklists_list(
            self.request, type="standard_advice", disable_pagination=True, show_deactivated=False
        )
    }


def proviso_picklist(self):
    return {
        "proviso": get_picklists_list(self.request, type="proviso", disable_pagination=True, show_deactivated=False)
    }


def footnote_picklist(self):
    return {
        "footnote_details": get_picklists_list(
            self.request, type="footnotes", disable_pagination=True, show_deactivated=False
        )
    }
