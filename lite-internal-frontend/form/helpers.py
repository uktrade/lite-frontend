import uuid
from enum import Enum


class Section:
    def __init__(self, title, description, forms):
        self.id = uuid.uuid1()
        self.title = title
        self.description = description
        self.forms = forms


class Form:
    def __init__(self, title, description, questions):
        self.id = uuid.uuid1()
        self.title = title
        self.description = description
        self.questions = questions


class Question:
    def __init__(self, title, description, input_type, name):
        self.id = uuid.uuid1()
        self.title = title
        self.description = description
        self.input_type = input_type
        self.name = name


class ArrayQuestion(Question):
    def __init__(self, title, description, input_type, name, data):
        super().__init__(title, description, input_type, name)
        self.data = data


class Option(Question):
    def __init__(self, key, value, sections=[]):
        self.key = key
        self.value = value
        self.sections = sections


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
