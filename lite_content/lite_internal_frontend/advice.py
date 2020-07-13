class AdvicePage:
    TEXT = "Reason"
    PROVISO = "Proviso"
    DENIAL_REASONS = "Denial reasons"
    NOTE = "Note"
    BY_PREFIX = "by "
    NO_ADVICE = "No advice given"


class UserAdvicePage:
    GIVE_CHANGE_ADVICE_BUTTON = "Give or change advice"
    CONTINUE_BUTTON = "Combine all into team advice"


class TeamAdvicePage:
    GIVE_CHANGE_ADVICE_BUTTON = "Give or change advice"
    CLEAR_ADVICE_BUTTON = "Clear advice"
    CONTINUE_BUTTON = "Combine all into final decision"


class FinalAdvicePage:
    GIVE_CHANGE_ADVICE_BUTTON = "Give or change advice"
    CLEAR_ADVICE_BUTTON = "Clear advice"
    FINALISE_BUTTON = "Finalise"
    FINALISED_GOODS_AND_COUNTRIES_BUTTON = "Finalise goods and countries"

    class WarningBanner:
        HIDDEN_ACCESSIBILITY_TEXT = "Warning"
        BLOCKING_FLAGS = "This application is blocked by the following flags: "


class GiveOrChangeAdvicePage:
    TITLE = "What do you advise?"
    WARNING = "The advice for your selected items does not match. However, you can still override the advice."
    PROVISO = "Proviso"
    PROVISO_DESCRIPTION = "This will appear on the generated documentation"
    DENIAL_REASONS_TITLE = "Select the appropriate denial reasons for your selection"
    GRADING_TITLE = "Select a grading"
    REASON = "What are your reasons for this decision?"
    NOTE = "Is there anything else you want to say to the applicant?"
    NOTE_DESCRIPTION = "This will appear on the generated documentation"
    GIVING_ADVICE_ON = "Giving advice on:"

    class Actions:
        CONTINUE_BUTTON = "Submit advice"
        BACK_BUTTON = "Back to advice"

    class RadioButtons:
        DESCRIPTION = "If you choose to refuse the licence, you must provide a reason for this decision"
        GRANT = "Grant the licence"
        PROVISO = "Add a proviso"
        NLR = "Tell the applicant they do not need a licence"
        NOT_APPLICABLE = "Not applicable"
        REJECT = "Reject the licence"
        REFUSE = "Refuse the licence"

    class FootNote:
        FOOTNOTE_REQUIRED = "Is a footnote required?"
        YES_OPTION = "Yes"
        NO_OPTION = "No"


class GenerateGoodsDecisionForm:
    TITLE = "Generate decision documents"
    NOTE = "Explain why you're making this decision (optional)"
    NOTE_DESCRIPTION = "Do this once you've generated your documents"
    SUCCESS_MESSAGE = "Case finalised"
    BUTTON = "Save and publish to exporter"


class GoodsDecisionMatrixPage:
    ERROR = "There is a problem"
    NO_ADVICE_DEFAULT = "No advice"
    REFUSE_ADVICE_TAG = "(Reject)"
    TITLE = "Select a decision for each good and country combination"

    class Table:
        GOODS = "Goods"
        DESTINATIONS = "Destinations"
        DECISION = "Decision"


class FinaliseLicenceForm:
    APPROVE_TITLE = "Approve"
    FINALISE_TITLE = "Finalise"
    DATE_DESCRIPTION = "For example, 27 3 2019"
    DATE_TITLE = "Licence start date"
    DURATION_DESCRIPTION = "This must be a whole number of months, such as 12"
    DURATION_TITLE = "How long will it last?"
    GOODS_ERROR = "Approved goods could not be fetched"

    class GoodsTable:
        CLC_COLUMN = "CLC"
        DESCRIPTION_COLUMN = "Description"
        DECISION_COLUMN = "Decision"
        LICENCED_QTY_COLUMN = "Licensed quantity"
        LICENCED_VALUE_COLUMN = "Licensed value"
        APPLIED_FOR_TEXT = "Applied for "
        PREVIOUSLY_LICENCED = "Previously licenced "
        USAGE = "Used "
        PROVISO_TEXT = "Proviso notes;"

    class Actions:
        BACK_TO_ADVICE_BUTTON = "Back to final advice"
        BACK_TO_DECISION_MATRIX_BUTTON = "Back to finalise goods and destinations"
