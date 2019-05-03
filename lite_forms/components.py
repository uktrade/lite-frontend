import uuid
from enum import Enum


class InputType(Enum):
    INPUT = 1
    TEXTAREA = 2
    NUMBER = 3
    SELECT = 4
    RADIOBUTTONS = 5
    CHECKBOXES = 6
    FILE_UPLOAD = 7
    MULTI_FILE_UPLOAD = 8
    AUTOCOMPLETE = 9
    HIDDEN = 10
    PASSWORD = 11
    CURRENCY = 12
    HEADING = 13
    HTML = 14


class ButtonStyle(Enum):
    DEFAULT = 'govuk-button'
    SECONDARY = 'govuk-button govuk-button--secondary'
    WARNING = 'govuk-button govuk-button--warning'


class HeadingStyle(Enum):
    XL = 1
    L = 2
    M = 3
    S = 4


class Button:
    def __init__(self, value, action, style=ButtonStyle.DEFAULT):
        self.value = value
        self.action = action
        self.style = style


class Section:
    def __init__(self, title, description, forms):
        self.id = uuid.uuid1()
        self.title = title
        self.description = description
        self.forms = forms


class Form:
    def __init__(self,
                 title,
                 description,
                 questions,
                 caption=None,
                 prefix=None,
                 buttons=None,
                 helpers=None,
                 javascript_imports=None):
        self.pk = uuid.uuid1()
        self.title = title
        self.description = description
        self.questions = questions
        self.questions.append(HiddenField(name='form_pk', value=self.pk))
        self.caption = caption
        self.helpers = helpers
        self.buttons = buttons
        if self.buttons is None:
            self.buttons = [Button('Submit', 'submit')]
        self.javascript_imports = javascript_imports
        self.prefix = prefix


class Question:
    def __init__(self, title, description, input_type, name, optional=False, prefix=None, extras=None):
        self.id = uuid.uuid1()
        self.title = title
        self.description = description
        self.input_type = input_type
        self.name = name
        self.optional = optional
        self.prefix = prefix
        self.extras = extras


class ArrayQuestion(Question):
    def __init__(self, title, description, input_type, name, data):
        super().__init__(title, description, input_type, name)
        self.data = data


class HiddenField:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.input_type = InputType.HIDDEN


class Option:
    def __init__(self, key, value, show_pane=None, sections=None):
        self.key = key
        self.value = value
        self.sections = sections
        self.show_pane = show_pane


class HelpSection:
    def __init__(self, title, description):
        self.title = title
        self.description = description


class HTMLBlock:
    def __init__(self, html):
        self.html = html
        self.input_type = InputType.HTML


class SideBySideSection:
    def __init__(self, questions):
        self.input_type = 'side_by_side'
        self.questions = questions


class Heading:
    def __init__(self, text, heading_style):
        self.text = text
        self.heading_style = heading_style
        self.input_type = InputType.HEADING
