from conf.constants import APPLICANT_EDITING


class ApplicationEditTypes:
    MINOR_EDIT = "minor_edit"
    MAJOR_EDIT = "major_edit"


def get_application_edit_type(application: dict):
    """
    Returns the application status type
    Possible return values are:
    * "minor_edit" - This application is in a minor edit state
    * "major_edit" - This application is in a major edit state
    * None - This application isn't being edited
    """
    if application["status"]:
        is_editing = application["status"]["key"] == "submitted" or application["status"]["key"] == APPLICANT_EDITING
        if is_editing:
            return (
                ApplicationEditTypes.MINOR_EDIT
                if application["status"]["key"] == "submitted"
                else ApplicationEditTypes.MAJOR_EDIT
            )
    return None
