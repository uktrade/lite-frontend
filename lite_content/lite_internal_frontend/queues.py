class QueuesList:
    TITLE = "Manage queues"
    CREATE_QUEUE_BUTTON = "Add a queue"
    NO_CONTENT_NOTICE = "There are no registered queues at the moment."

    class Table:
        NAME = "Name"
        TEAM = "Team"
        ACTIONS = "Actions"
        EDIT = "Edit"
        VIEW_CASES = "View cases"


class AddQueueForm:
    TITLE = "Add a queue"
    DESCRIPTION = ""
    BACK = "Back to queues"

    class Name:
        TITLE = "Name"
        DESCRIPTION = ""


class EditQueueForm:
    TITLE = "Edit queue"
    DESCRIPTION = ""
    BACK = "Back to queues"

    class Name:
        TITLE = "Name"
        DESCRIPTION = ""
