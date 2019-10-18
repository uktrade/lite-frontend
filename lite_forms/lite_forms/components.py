from lite_forms.styles import ButtonStyle


class _Component:
    """
    Base component for LITE forms - only for internal use
    """

    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None,
                 extras=None):
        self.name = name
        self.title = title
        self.description = description
        self.optional = optional
        self.classes = classes
        self.extras = extras


class Button:
    def __init__(self, value, action, style=ButtonStyle.DEFAULT, link=None, float_right=False):
        self.value = value
        self.action = action
        self.style = style
        self.link = link
        self.float_right = float_right


class BackLink:
    def __init__(self, text='Back', url='#'):
        self.text = text
        self.url = url


class FormGroup:
    """
    Container for multiple forms
    Automatically adds IDs to all forms to make it easier to reference them
    """
    def __init__(self, forms: list, show_progress_indicators=False):
        self._forms = forms
        self.show_progress_indicators = show_progress_indicators

        self.update_progress_indicators()
        self.update_pks()

    def get_forms(self):
        return [x for x in self._forms if x is not None]

    def set_forms(self, value):
        self._forms = value

    forms = property(get_forms, set_forms)

    def update_progress_indicators(self):
        index = 0
        if self.show_progress_indicators:
            for form in self.forms:
                if form:
                    form.caption = f'Step {index + 1} of {len(self.forms)}'
                    index += 1

    def update_pks(self):
        index = 0
        for form in self.forms:
            if form:
                form.pk = index
                form.questions.append(HiddenField(name='form_pk', value=form.pk))
                index += 1


class Label:
    def __init__(self, text: str):
        self.text = text
        self.input_type = 'label'


class Form:
    def __init__(self,
                 title=None,
                 description=None,
                 questions=None,
                 caption=None,
                 buttons=None,
                 helpers=None,
                 footer_label: Label = None,
                 javascript_imports=None,
                 default_button_name='Submit',
                 back_link=BackLink(),
                 post_url=None):
        self.title = title
        self.description = description
        self.questions = questions
        self.caption = caption
        self.helpers = helpers
        self.footer_label = footer_label
        self.buttons = buttons
        self.back_link = back_link
        if self.buttons is None:
            self.buttons = [Button(default_button_name, 'submit')]
        self.javascript_imports = javascript_imports
        self.post_url = post_url


class DetailComponent:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.input_type = 'detail'


class HiddenField:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.input_type = 'hidden'


class HelpSection:
    def __init__(self, title, description):
        self.title = title
        self.description = description


class HTMLBlock:
    def __init__(self, html):
        self.html = html
        self.input_type = 'html_block'


class SideBySideSection:
    def __init__(self, questions):
        self.input_type = 'side_by_side'
        self.questions = questions


class TextInput(_Component):
    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        super().__init__(name, title, description, optional, classes)
        self.input_type = 'text_input'


class NumberInput(_Component):
    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        super().__init__(name, title, description, optional, classes)
        self.input_type = 'number_input'


class QuantityInput(_Component):
    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        super().__init__(name, title, description, optional, classes)
        self.input_type = 'quantity_input'


class PasswordInput(_Component):
    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        super().__init__(name, title, description, optional, classes)
        self.input_type = 'password_input'


class CurrencyInput(_Component):
    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        super().__init__(name, title, description, optional, classes)
        self.input_type = 'currency_input'


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
                 classes: [] = None,
                 empty_notice: str = 'No items'):
        super().__init__(name, title, description, optional, classes)
        self.options = options
        self.empty_notice = empty_notice
        self.input_type = 'checkboxes'


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
                 classes: [] = None,
                 empty_notice: str = 'No items'):
        super().__init__(name, title, description, optional, classes)
        self.options = options
        self.empty_notice = empty_notice
        self.input_type = 'radiobuttons'


class Select(_Component):
    def __init__(self,
                 name: str,
                 options: [],
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None,
                 include_default_select: bool = True):
        super().__init__(name, title, description, optional, classes)
        self.options = options
        self.input_type = 'select'
        self.include_default_select = include_default_select


class Option:
    def __init__(self, key, value, description=None, show_pane=None, sections=None, show_or=False):
        self.key = key
        self.value = value
        self.description = description
        self.sections = sections
        self.show_pane = show_pane
        self.show_or = show_or


class Group:
    """
    Groups components together inside of a div
    """

    def __init__(self, name, components):
        self.input_type = 'group'
        self.name = name
        self.components = components


class Filter:
    """
    Filters a list of checkboxes based on title and description
    """

    def __init__(self, placeholder: str = 'Filter'):
        """
        :type placeholder: Sets the placeholder text on the input field
        """
        self.placeholder = placeholder
        self.input_type = 'filter'


class Heading:
    def __init__(self, text, heading_style):
        self.text = text
        self.heading_style = heading_style
        self.input_type = 'heading'


class FileUpload(_Component):
    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        super().__init__(name, title, description, optional, classes)
        self.input_type = 'file_upload'


class MultiFileUpload(_Component):
    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        super().__init__(name, title, description, optional, classes)
        self.input_type = 'multi_file_upload'


class TextArea(_Component):
    def __init__(self,
                 name: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None,
                 extras: [] = None):
        super().__init__(name, title, description, optional, classes, extras)
        self.input_type = 'textarea'


class MarkdownArea(_Component):
    def __init__(self,
                 name: str,
                 variables: [],
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None,
                 extras: [] = None):
        super().__init__(name, title, description, optional, classes, extras)
        self.variables = variables
        self.input_type = 'markdown'


class DateInput:
    def __init__(self,
                 prefix: str,
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None,
                 extras: [] = None):
        self.prefix = prefix
        self.title = title
        self.description = description
        self.optional = optional
        self.classes = classes
        self.extras = extras
        self.input_type = 'date'


class Summary:
    def __init__(self,
                 values: dict = None,
                 classes: [] = None,
                 extras: [] = None):
        self.values = values
        self.classes = classes
        self.extras = extras
        self.input_type = 'summary'


class ControlListEntryInput:
    def __init__(self,
                 name: str,
                 options: [],
                 title: str = '',
                 description: str = '',
                 optional: bool = False,
                 classes: [] = None):
        self.name = name
        self.title = title
        self.description = description
        self.options = options
        self.optional = optional
        self.classes = classes
        self.input_type = 'control_list_entry'
