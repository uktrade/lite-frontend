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
    DETAIL = 15
    FILTER = 16
    QUANTITY = 17


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
        self.title = title
        self.description = description
        self.forms = forms


class BackLink:
    def __init__(self, text='Back', url='#'):
        self.text = text
        self.url = url


class Form:
    def __init__(self,
                 title,
                 description,
                 questions,
                 caption=None,
                 buttons=None,
                 helpers=None,
                 javascript_imports=None,
                 default_button_name='Submit',
                 pk=None,
                 back_link=BackLink()):

        if not pk:
            self.pk = uuid.uuid1()
        else:
            self.pk = pk

        self.title = title
        self.description = description
        self.questions = questions
        self.questions.append(HiddenField(name='form_pk', value=self.pk))
        self.caption = caption
        self.helpers = helpers
        self.buttons = buttons
        self.back_link = back_link
        if self.buttons is None:
            self.buttons = [Button(default_button_name, 'submit')]
        self.javascript_imports = javascript_imports


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
    def __init__(self, title, description, input_type, name, data, same_row=False):
        super().__init__(title, description, input_type, name)
        self.same_row = same_row
        self.data = data


class DetailComponent:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.input_type = InputType.DETAIL


class HiddenField:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.input_type = InputType.HIDDEN


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


class _Component:
    """
    Base component for LITE forms - only for internal use
    """

    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        self.name = name
        self.title = title
        self.description = description
        self.optional = optional
        self.classes = classes


class Input(_Component):
    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        super().__init__(name, title, description, optional, classes)
        self.input_type = 'INPUT'


class Checkboxes(_Component):
    """
    Displays checkboxes on the page
    Add Option components to the options array to show checkboxes
    Add optional classes such as 'lite-checkboxes--inline' or 'govuk-checkboxes--small'
    """

    def __init__(self,
                 name: str,
                 options: [],
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        super().__init__(name, title, description, optional, classes)
        self.options = options
        self.input_type = 'CHECKBOXES'


class RadioButtons(_Component):
    """
    Displays radiobuttons on the page
    Add Option components to the options array to show radiobuttons
    Add optional classes such as 'lite-radiobuttons--inline' or 'govuk-radiobuttons--small'
    """

    def __init__(self,
                 name: str,
                 options: [],
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        super().__init__(name, title, description, optional, classes)
        self.options = options
        self.input_type = 'RADIOBUTTONS'


class Option:
    def __init__(self, key, value, description=None, show_pane=None, sections=None, show_or=False):
        self.key = key
        self.value = value
        self.description = description
        self.sections = sections
        self.show_pane = show_pane
        self.show_or = show_or


class Filter:
    """
    Filters a list of checkboxes based on title and description
    """

    def __init__(self, placeholder: str = 'Filter'):
        """
        :type placeholder: Sets the placeholder text on the input field
        """
        self.placeholder = placeholder
        self.input_type = InputType.FILTER


class Heading:
    def __init__(self, text, heading_style):
        self.text = text
        self.heading_style = heading_style
        self.input_type = InputType.HEADING
