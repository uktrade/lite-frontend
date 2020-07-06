import json
from json import JSONDecodeError

from django.template.defaulttags import register
from django.urls import reverse
from django.utils.safestring import mark_safe

from core.builtins.custom_tags import get_const_string
from lite_forms.helpers import convert_to_markdown, flatten_data


@register.filter
def has_attribute(_object, attribute):
    return hasattr(_object, attribute)


@register.filter
def component_name(data, _object):
    name = getattr(_object, "name", None)
    return flatten_data(data).get(name)


@register.filter
def key_value(dictionary, key):
    if not dictionary:
        return

    try:
        if key.endswith("[]"):
            key = key[:-2]
    # This allows defaultdicts to pass through unaffected as their keys
    # do not have the endswith attribute
    except AttributeError:
        pass

    value = dictionary.get(key)

    try:
        if isinstance(value, str):
            value = json.loads(value)
    except JSONDecodeError:
        pass

    return value


@register.filter
def has_components(component_options):
    for item in component_options:
        if getattr(item, "components", None):
            return True


@register.filter
def key_in_array(data, key):
    if data is None:
        return False

    if isinstance(data, str):
        if str(key) == data:
            return True
        return False

    if isinstance(data, bool) and isinstance(key, bool):
        return data == key

    if isinstance(data, bool):
        return data

    # If data is a dict, check the id
    if isinstance(data, dict):
        if "id" in data:
            return data["id"] == key
        if "key" in data:
            return data["key"] == key

    # If data is a list, check for the key
    if isinstance(data, list):
        if key in data:
            return True

        for item in data:
            if isinstance(item, str):
                if item == key:
                    return True
            else:
                if item.get("id") == key:
                    return True

    return False


@register.filter
def prefix_dots(text):
    """
    Prefix dots in an ID so it can be used in a jQuery selector.

    See https://stackoverflow.com/a/9930611
    """
    return text.replace(".", r"\\.")


@register.filter
def replace_spaces(text):
    """
    Replace spaces with a dash.
    """
    return text.replace(" ", "-")


@register.simple_tag
@mark_safe
def dict_hidden_field(key, value):
    """
    Generates a hidden field from the given key and value
    """
    if isinstance(value, dict):
        value = json.dumps(value)
    if isinstance(value, list):
        str = ""
        for item in value:
            str += f"<input type='hidden' name='{key}[]' value='{item}'>"
        return str
    return f"<input type='hidden' name='{key}' value='{value}'>"


@register.filter
def classname(obj):
    """
    Returns object class name
    """
    return obj.__class__.__name__


@register.filter
def date_join(data, prefix):
    if data:
        date = dict()
        prefix_length = len(prefix)
        for key, value in data.items():
            if value and prefix in key:
                string = key[prefix_length:]
                if string == "day":
                    date["day"] = value
                elif string == "month":
                    date["month"] = value
                elif string == "year":
                    date["year"] = value
        return date


@register.filter
def get(value, arg):
    return value.get(arg, "") if value else None


@register.filter
@mark_safe
def markdown(text):
    return convert_to_markdown(text)


@register.filter
def heading_class(text):
    if text and len(text) < 150:
        return "govuk-fieldset__legend--xl"

    return "govuk-fieldset__legend--l"


@register.filter
def file_type(file_name):
    """
    Returns the file type from a complete file name
    If the file doesn't have a file type, return "file"
    """
    if "." not in file_name:
        return "file"

    return file_name.split(".")[-1]


@register.simple_tag
def make_list(*args):
    return args


@register.filter
def pagination_params(url, page):
    import urllib.parse as urlparse
    from urllib.parse import urlencode

    url_parts = list(urlparse.urlparse(url))
    query_params = dict(urlparse.parse_qsl(url_parts[4]))
    query_params.pop("page", 1)
    query = {"page": page, **query_params}
    url_parts[4] = urlencode(query)

    return urlparse.urlunparse(url_parts)


@register.filter()
def item_with_rating_exists(items, rating):
    if not items:
        return

    for item in items:
        if isinstance(item, str):
            if item == rating:
                return True

        if isinstance(item, dict):
            if item["rating"] == rating:
                return True


@register.simple_tag
@mark_safe
def govuk_link_button(text, url, url_param=None, id="", classes="", query_params="", show_chevron=False):
    text = get_const_string(text)
    if isinstance(url_param, str):
        url_param = [url_param]
    url = reverse(url, args=url_param if url_param else [])
    id = f'id="button-{id}"' if id else ""
    chevron = ""
    if show_chevron:
        chevron = (
            '<svg class="govuk-button__start-icon" xmlns="http://www.w3.org/2000/svg" width="13" height="15" '
            'viewBox="0 0 33 43" aria-hidden="true" focusable="false">'
            '<path fill="currentColor" d="M0 0h13l20 20-20 20H0l20-20z" /></svg>'
        )

    return (
        f'<a {id} href="{url}{query_params}" role="button" draggable="false" class="govuk-button {classes}" '
        f'data-module="govuk-button">{text}{chevron}</a>'
    )


@register.inclusion_tag("components/pagination.html", takes_context=True)
def pagination(context, *args, **kwargs):
    class PageItem:
        def __init__(self, number, url, selected=False):
            self.number = number
            self.url = url
            self.selected = selected
            self.type = "page_item"

    class PageEllipsis:
        def __init__(self, text="..."):
            self.text = text
            self.type = "page_ellipsis"

    if "data" not in kwargs:
        data = context["data"] if "data" in context else context
    else:
        data = kwargs["data"]

    # If the data provided isn't
    if not data or "total_pages" not in data:
        return

    request = context["request"]
    current_path = request.get_full_path()
    current_page = int(context["request"].GET.get("page", 1))
    max_pages = int(data["total_pages"])
    max_range = 5
    pages = []

    # We want there to be a max_range bubble around the current page
    # eg current page is 6 and max range is 4, therefore we'll see 2 3 4 5 6 7 8 9 10
    start_range = max(1, current_page - max_range)
    end_range = min(max_pages, current_page + max_range)

    # Account for starting at 1, instead of 0
    if (start_range - 2) <= 1:
        start_range = 1
    else:
        pages.insert(0, PageItem(1, pagination_params(current_path, 1)))
        pages.insert(1, PageEllipsis())

    # UX: If end range + 2 (2 representing an ellipsis and final element) just show the last
    # two pages as well
    if (end_range + 2) >= max_pages:
        end_range = max_pages

    # Account for starting at 1, instead of 0
    end_range += 1

    # Add page items
    for i in range(start_range, end_range):
        pages.append(PageItem(i, pagination_params(current_path, i), i == current_page))

    # If current page + max range is more than two pages away from the last page, show an ellipsis
    if current_page + max_range < max_pages - 2:
        pages.append(PageEllipsis())
        pages.append(PageItem(max_pages, pagination_params(current_path, max_pages)))

    context["previous_link_url"] = pagination_params(current_path, current_page - 1) if current_page != 1 else None
    context["next_link_url"] = pagination_params(current_path, current_page + 1) if current_page != max_pages else None
    context["pages"] = pages

    return context
