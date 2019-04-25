import uuid
from enum import Enum


class Section:
    def __init__(self, title, description, forms):
        self.id = uuid.uuid1()
        self.title = title
        self.description = description
        self.forms = forms


class Form:
    def __init__(self, title, description, questions, caption=None, helpers=None):
        self.id = uuid.uuid1()
        self.title = title
        self.description = description
        self.questions = questions
        self.helpers = helpers
        self.caption = caption


class Question:
    def __init__(self, title, description, input_type, name, extras=None):
        self.id = uuid.uuid1()
        self.title = title
        self.description = description
        self.input_type = input_type
        self.name = name
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
