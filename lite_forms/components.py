from enum import Enum

from django.conf import settings
from typing import List, Optional, Dict, Set

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
        self,
        text: str,
        id: str = None,
        classes: Optional[List] = None,
    ):
        from lite_forms.helpers import convert_to_markdown

        self.id = id
        self.text = convert_to_markdown(text)
        self.classes = classes
        self.input_type = "label"


class EmptyLabel:
    def __init__(
        self,
        id: str = None,
        classes: Optional[List] = None,
    ):

        self.id = id
        self.text = ""
        self.classes = classes
        self.input_type = "label"


class GroupWithLabel(_Component):
    def __init__(
        self,
        text: str = None,
        id: str = None,
        components: Optional[List] = None,
        classes: Optional[List] = None,
    ):
        super().__init__(text, classes)
        self.id = id
        self.components = [EmptyLabel()] + components
        self.classes = classes
        self.input_type = "group"


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
        javascript_imports: Optional[Set[str]] = None,
        default_button_name="Save",
        default_button_style=ButtonStyle.DEFAULT,
        back_link=BackLink(),
        post_url=None,
        container: str = "two-pane",
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
        self.javascript_imports = javascript_imports or set()
        self.post_url = post_url
        self.single_form_element = heading_used_as_label(questions)
        self.container = container
        from lite_forms.helpers import get_all_form_components

        if self.questions:
            for component in get_all_form_components(self):
                for item in getattr(component, "javascript_imports", []):
                    self.javascript_imports.add(item)

    def __str__(self):
        return f'{self.__class__.__module__}.{self.__class__.__name__}(title="{self.title}")'


class DetailComponent:
    def __init__(self, title, description="", components=None):
        from lite_forms.helpers import convert_to_markdown

        self.title = title
        self.description = convert_to_markdown(description)
        self.components = components
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


class EmailInput(_Component):
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
        self.input_type = "email_input"


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
        short_title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        empty_notice: str = "No items",
        show_select_links: bool = False,
        disabled_hint: str = "",
        filterable: bool = False,
        import_custom_js: list = None,
    ):
        super().__init__(
            name=name,
            title=title,
            short_title=short_title,
            description=description,
            accessible_description=accessible_description,
            optional=optional,
            classes=classes,
        )
        self.options = options
        self.disabled_hint = disabled_hint
        self.empty_notice = empty_notice
        self.show_select_links = show_select_links
        self.input_type = "checkboxes"
        self.javascript_imports = ["/javascripts/select-links.js"]
        if filterable:
            self.javascript_imports.append("/javascripts/filter-checkbox-list.js")
        if import_custom_js:
            self.javascript_imports.extend(import_custom_js)


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
        filterable: bool = False,
    ):
        super().__init__(name, title, description, short_title, accessible_description, optional, classes)
        self.options = options
        self.empty_notice = empty_notice
        self.input_type = "radiobuttons"
        self.javascript_imports = []
        if filterable:
            self.javascript_imports.append("/javascripts/filter-radiobuttons-list.js")


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
    ):
        super().__init__(name, options, title, description, accessible_description, optional, classes, empty_notice)
        self.input_type = "radiobuttons_image"


class Select(_Component):
    def __init__(
        self,
        name: str,
        options: List,
        title: str = "",
        initial: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        include_default_select: bool = True,
    ):
        super().__init__(name, title, description, accessible_description, optional, classes)
        self.options = options
        self.initial = initial
        self.input_type = "select"
        self.include_default_select = include_default_select


class Option:
    def __init__(
        self,
        key,
        value,
        description=None,
        show_or=False,
        img_url=None,
        auto_check=True,
        components=None,
        data_attribute=None,
        classes: Optional[List] = None,
        more_information: str = None,
        tag: str = None,
        disabled: bool = False,
        cannot_remove: bool = False,
        id=None,
    ):
        from lite_forms.helpers import convert_to_markdown

        self.auto_check = auto_check
        self.key = key
        self.value = value
        self.description = convert_to_markdown(description)
        self.show_or = show_or
        self.img_url = img_url
        self.components = [component for component in components if component] if components else []
        self.data_attribute = data_attribute
        self.classes = classes
        self.more_information = more_information
        self.tag = tag
        self.disabled = disabled
        self.cannot_remove = cannot_remove
        self.id = id


class Group:
    """
    Groups components together inside of a div
    """

    def __init__(self, id, components, classes=None):
        self.input_type = "group"
        self.id = id
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
        name: str = "file",
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        accept: Optional[List] = None,
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
        self.accept = accept or settings.ACCEPTED_FILE_UPLOAD_MIME_TYPES


class TextArea(_Component):
    def __init__(
        self,
        name: str,
        title: str = "",
        short_title: str = None,
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        extras: Optional[Dict] = None,
        rows: int = 10,
        data_attributes: Optional[Dict] = None,
    ):
        super().__init__(
            name=name,
            title=title,
            short_title=short_title,
            description=description,
            accessible_description=accessible_description,
            optional=optional,
            classes=classes,
            extras=extras,
        )
        self.rows = rows
        self.data_attributes = data_attributes
        self.input_type = "textarea"


class MarkdownArea(TextArea):
    def __init__(
        self,
        name: str,
        title: str = "",
        description: str = "",
        accessible_description: str = None,
        optional: bool = False,
        classes: Optional[List] = None,
        extras: Optional[Dict] = None,
    ):
        super().__init__(name, title, description, accessible_description, optional, classes, extras)
        self.input_type = "markdown"


class DateInput:
    def __init__(
        self,
        prefix: str,
        title: str = "",
        inline_title: bool = False,
        short_title: str = None,
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
        self.short_title = short_title
        self.inline_title = inline_title


class Summary:
    def __init__(self, values: dict = None, classes: Optional[List] = None, extras: Optional[List] = None):
        self.values = values
        self.classes = classes
        self.extras = extras
        self.input_type = "summary"


class TreeNode:
    def __init__(self, key, value, children=None):
        self.key = key
        self.value = value
        self.children = children if children else []


class TreeView:
    def __init__(self, name, data: List, title="", short_title=""):
        self.title = title
        self.short_title = short_title or title
        self.name = name
        self.data = TreeNode("", "", data)
        self.input_type = "tree-view"


class List:
    class ListType(Enum):
        DEFAULT = 1
        BULLETED = 2
        NUMBERED = 3

    def __init__(
        self,
        items: [],
        title: str = None,
        type: ListType = ListType.DEFAULT,
        classes: Optional[List] = None,
    ):
        self.items = items
        self.title = title
        self.type = type
        self.classes = classes
        self.input_type = "list"


class TokenBar:
    def __init__(
        self,
        name: str,
        options: [],
        title: str = "",
        description: str = "",
        optional: bool = False,
        classes: [] = None,
    ):
        """
        TokenBar allows for input of complex pieces of information in compact form,
        such as an entity (person, place, or thing) or text. They enable user input and
        verify that input by converting text into chips.
        """
        from lite_forms.helpers import convert_to_markdown

        self.name = name
        self.title = title
        self.description = convert_to_markdown(description)
        self.options = options
        self.optional = optional
        self.classes = classes if classes else ["tokenfield-container"]
        self.input_type = "token-bar"
        self.javascript_imports = ["/javascripts/tokenfield.min.js"]


class AutocompleteInput:
    def __init__(
        self,
        name: str,
        options: List,
        title: str = "",
        initial: str = "",
        description: str = "",
        classes: Optional[List] = None,
        deferred: bool = False,
    ):
        self.name = name
        self.title = title
        self.initial = initial
        self.description = description
        self.options = options
        self.classes = classes
        self.deferred = deferred
        self.input_type = "autocomplete"
        self.javascript_imports = ["/javascripts/accessible-autocomplete.min.js"]


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
        return getattr(other, "text", None) == self.text and getattr(other, "address", None) == self.address


class FiltersBar:
    def __init__(self, filters: List, advanced_filters: Optional[List] = None):
        self.filters = filters or []
        self.advanced_filters = advanced_filters or []
        self.javascript_imports = {"/javascripts/filter-bar.js"}
        for component in [*self.filters, *self.advanced_filters]:
            for item in getattr(component, "javascript_imports", []):
                self.javascript_imports.add(item)


class Custom:
    def __init__(self, template, data=None):
        self.input_type = "custom"
        self.data = data
        self.template = template


class WarningBanner:
    def __init__(self, id, text):
        self.input_type = "warning"
        self.id = id
        self.text = text
