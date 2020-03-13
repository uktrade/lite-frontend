from enum import Enum
from typing import List, Optional

from lite_forms.styles import ButtonStyle


class _Component:
    """
    Base component for LITE forms - only for internal use
    """

    def __init__(
        self,
        name: str,
        title: str = "",
        description: str = "",
        short_title: str = None,
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        extras=None,
    ):
        from lite_forms.helpers import convert_to_markdown

        self.name = name
        self.title = title
        self.description = convert_to_markdown(description)
        self.short_title = short_title or title
        self.accessible_description = accessible_description
        self.optional = optional
        self.classes = classes
        self.extras = extras


class Button:
    def __init__(
        self,
        value,
        action,
        style=ButtonStyle.DEFAULT,
        id=None,
        link=None,
        float_right=False,
        disable_double_click=False,
    ):
        self.value = value
        self.action = action
        self.style = style
        self.link = link
        if not id:
            self.id = value
        else:
            self.id = id
        self.float_right = float_right
        self.disable_double_click = disable_double_click


class BackLink:
    def __init__(self, text="Back", url="#"):
        self.text = text
        self.url = url


class Breadcrumbs:
    def __init__(self, back_links: List[BackLink]):  # noqa
        self.back_links = back_links


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
                    form.caption = f"Step {index + 1} of {len(self.forms)}"
                    index += 1

    def update_pks(self):
        index = 0
        for form in self.forms:
            if form:
                form.pk = index
                form.questions.append(HiddenField(name="form_pk", value=form.pk))
                index += 1


class Label:
    def __init__(
        self, text: str, id: str = None, classes: Optional[List] = None,
    ):
        from lite_forms.helpers import convert_to_markdown

        self.id = id
        self.text = convert_to_markdown(text)
        self.classes = classes
        self.input_type = "label"


class Form:
    def __init__(
        self,
        title=None,
        description=None,
        questions=None,
        caption=None,
        buttons=None,
        helpers=None,
        footer_label: Label = None,
        javascript_imports=None,
        default_button_name="Save",
        default_button_style=ButtonStyle.DEFAULT,
        back_link=BackLink(),
        post_url=None,
    ):
        from lite_forms.helpers import convert_to_markdown, heading_used_as_label

        self.title = title
        self.description = convert_to_markdown(description)
        self.questions = questions
        self.caption = caption
        self.helpers = helpers
        self.footer_label = footer_label
        self.buttons = buttons
        self.back_link = back_link
        if self.buttons is None:
            self.buttons = [Button(default_button_name, "submit", style=default_button_style)]
        self.javascript_imports = javascript_imports
        self.post_url = post_url
        self.single_form_element = heading_used_as_label(questions)


class DetailComponent:
    def __init__(self, title, description):
        from lite_forms.helpers import convert_to_markdown

        self.title = title
        self.description = convert_to_markdown(description)
        self.input_type = "detail"


class HiddenField:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.input_type = "hidden"


class HelpSection:
    def __init__(self, title, description, includes=None):
        from lite_forms.helpers import convert_to_markdown

        self.title = title
        self.description = convert_to_markdown(description)
        self.includes = includes


class HTMLBlock:
    def __init__(self, html):
        self.html = html
        self.input_type = "html_block"


class SideBySideSection:
    def __init__(self, questions):
        self.input_type = "side_by_side"
        self.questions = questions


class TextInput(_Component):
    def __init__(
        self,
        name: str,
        title: str = "",
        description: str = "",
        short_title: str = None,
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
    ):
        super().__init__(name, title, description, short_title, accessible_description, optional, classes)
        self.input_type = "text_input"


class NumberInput(_Component):
    def __init__(
        self,
        name: str,
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
    ):
        super().__init__(name, title, description, accessible_description, optional, classes)
        self.input_type = "number_input"


class QuantityInput(_Component):
    def __init__(
        self,
        name: str,
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
    ):
        super().__init__(name, title, description, accessible_description, optional, classes)
        self.input_type = "quantity_input"


class CurrencyInput(_Component):
    def __init__(
        self,
        name: str,
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
    ):
        super().__init__(name, title, description, accessible_description, optional, classes)
        self.input_type = "currency_input"


class Checkboxes(_Component):
    """
    Displays checkboxes on the page
    Add Option components to the options array to show checkboxes
    Add optional classes such as 'govuk-checkboxes--inline' or 'govuk-checkboxes--small'
    """

    def __init__(
        self,
        name: str,
        options: [],
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        empty_notice: str = "No items",
        show_select_links: bool = False,
    ):
        super().__init__(name=name,
                         title=title,
                         description=description,
                         accessible_description=accessible_description,
                         optional=optional,
                         classes=classes)
        self.options = options
        self.empty_notice = empty_notice
        self.show_select_links = show_select_links
        self.input_type = "checkboxes"


class RadioButtons(_Component):
    """
    Displays radiobuttons on the page
    Add Option components to the options array to show radiobuttons
    Add optional classes such as 'lite-radios--inline' or 'govuk-radios--small'
    """

    def __init__(
        self,
        name: str,
        options: List,
        title: str = "",
        description: str = "",
        short_title: str = None,
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        empty_notice: str = "No items",
    ):
        super().__init__(name, title, description, short_title, accessible_description, optional, classes)
        self.options = options
        self.empty_notice = empty_notice
        self.input_type = "radiobuttons"


class RadioButtonsImage(RadioButtons):
    """
    Displays radiobuttons on the page as images
    Add Option components to the options array to show radiobuttons
    Add optional classes such as 'lite-radiobuttons--inline' or 'govuk-radiobuttons--small'
    """

    def __init__(
        self,
        name: str,
        options: List,
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        empty_notice: str = "No items",
        total_pages: int = 1,
    ):
        super().__init__(name, options, title, description, accessible_description, optional, classes, empty_notice)
        self.total_pages = total_pages
        self.input_type = "radiobuttons_image"


class Select(_Component):
    def __init__(
        self,
        name: str,
        options: List,
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        include_default_select: bool = True,
    ):
        super().__init__(name, title, description, accessible_description, optional, classes)
        self.options = options
        self.input_type = "select"
        self.include_default_select = include_default_select


class Option:
    def __init__(
        self,
        key,
        value,
        description=None,
        show_pane=None,
        show_or=False,
        img_url=None,
        auto_check=True,
        components=None,
    ):
        from lite_forms.helpers import convert_to_markdown

        self.auto_check = auto_check
        self.key = key
        self.value = value
        self.description = convert_to_markdown(description)
        self.show_pane = show_pane  # DEPRECATED, use components instead
        self.show_or = show_or
        self.img_url = img_url
        self.components = components


class Group:
    """
    Groups components together inside of a div
    """

    def __init__(self, name, components, classes):
        self.input_type = "group"
        self.name = name
        self.components = components
        self.classes = classes


class Filter:
    """
    Filters a list of checkboxes based on title and description
    """

    def __init__(self, placeholder: str = "Filter"):
        """
        :type placeholder: Sets the placeholder text on the input field
        """
        self.placeholder = placeholder
        self.input_type = "filter"


class Heading:
    def __init__(self, text, heading_style):
        self.text = text
        self.heading_style = heading_style
        self.input_type = "heading"


class FileUpload(_Component):
    def __init__(
        self,
        name: str,
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
    ):
        super().__init__(
            name=name,
            title=title,
            description=description,
            accessible_description=accessible_description,
            optional=optional,
            classes=classes,
        )
        self.input_type = "file_upload"


class MultiFileUpload(_Component):
    def __init__(
        self,
        name: str,
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
    ):
        super().__init__(
            name=name,
            title=title,
            description=description,
            accessible_description=accessible_description,
            optional=optional,
            classes=classes,
        )
        self.input_type = "multi_file_upload"


class TextArea(_Component):
    def __init__(
        self,
        name: str,
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        extras: Optional[List] = None,
    ):
        super().__init__(
            name=name,
            title=title,
            description=description,
            accessible_description=accessible_description,
            optional=optional,
            classes=classes,
            extras=extras,
        )
        self.input_type = "textarea"


class MarkdownArea(TextArea):
    def __init__(
        self,
        name: str,
        variables: List,
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        extras: Optional[List] = None,
    ):
        super().__init__(name, title, description, accessible_description, optional, classes, extras)
        self.variables = variables
        self.input_type = "markdown"


class DateInput:
    def __init__(
        self,
        prefix: str,
        title: str = "",
        description: str = "",
        name: str = None,
        optional: bool = None,
        classes: Optional[List] = None,
        extras: Optional[List] = None,
    ):
        from lite_forms.helpers import convert_to_markdown

        self.prefix = prefix
        self.title = title
        self.description = convert_to_markdown(description)
        self.name = name
        self.optional = optional
        self.classes = classes
        self.extras = extras
        self.input_type = "date"


class Summary:
    def __init__(self, values: dict = None, classes: Optional[List] = None, extras: Optional[List] = None):
        self.values = values
        self.classes = classes
        self.extras = extras
        self.input_type = "summary"


class List:
    class ListType(Enum):
        DEFAULT = 1
        BULLETED = 2
        NUMBERED = 3

    def __init__(
        self, items: [], title: str = None, type: ListType = ListType.DEFAULT, classes: Optional[List] = None,
    ):
        self.items = items
        self.title = title
        self.type = type
        self.classes = classes
        self.input_type = "list"


class ControlListEntryInput:
    def __init__(
        self,
        name: str,
        options: [],
        title: str = "",
        description: str = "",
        optional: bool = False,
        classes: [] = None,
    ):
        from lite_forms.helpers import convert_to_markdown

        self.name = name
        self.title = title
        self.description = convert_to_markdown(description)
        self.options = options
        self.optional = optional
        self.classes = classes
        self.input_type = "control_list_entry"


class AutocompleteInput:
    def __init__(self, name: str, options: List, title: str = ""):
        self.name = name
        self.options = options
        self.title = title
        self.input_type = "autocomplete"


class Link:
    def __init__(
        self, text: str, address: str, name: str = None, classes: Optional[List] = None, form_action: bool = False
    ):
        self.text = text
        self.address = address
        self.name = name
        self.classes = classes
        self.form_action = form_action
        self.input_type = "link"

    def __eq__(self, other):
        return other.text == self.text and other.address == self.address


class FiltersBar:
    def __init__(self, filters: list):
        self.filters = filters
