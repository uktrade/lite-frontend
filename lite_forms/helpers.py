import copy
from collections.abc import MutableMapping

from markdown import markdown

from lite_forms.components import FormGroup, Form, HiddenField, TreeNode


def get_form_by_pk(form_pk, form_group: FormGroup):
    for form in form_group.forms:
        if str(form.pk) == str(form_pk):
            return copy.deepcopy(form)


def get_previous_form(form_pk, form_group: FormGroup):
    for form in form_group.forms:
        # If the current form is the final form in the group
        if int(form.pk) == int(form_pk) - 1:
            return copy.deepcopy(form)


def get_next_form(form_pk, form_group: FormGroup):
    next_one = False
    for form in form_group.forms:
        if next_one:
            return copy.deepcopy(form)
        if str(form.pk) == str(form_pk):
            next_one = True


def remove_unused_errors(errors, form: Form):
    """
    Removes all errors that don't belong to a form's fields
    :param errors: ['errors'] children
    :param form: Form object
    :return: Array of cleaned errors
    """
    cleaned_errors = {}

    if errors.get("non_field_errors"):
        cleaned_errors["non_field_errors"] = errors.get("non_field_errors")

    if not errors:
        return {}

    for component in get_all_form_components(form):
        # we look at [:-2] since checkboxes are lists that are named like "field[]", and we don't have "[]" in the api
        list_components = ["checkboxes", "tree-view"]
        if (
            hasattr(component, "input_type")
            and component.input_type in list_components
            and errors.get(component.name[:-2])
        ):
            cleaned_errors[component.name[:-2]] = errors.get(component.name[:-2])
        elif hasattr(component, "name") and errors.get(component.name):
            cleaned_errors[component.name] = errors.get(component.name)
        elif hasattr(component, "input_type") and component.input_type == "group" and errors.get(component.id):
            # update label class to show as error
            label = component.components[0]
            if hasattr(label, "text"):
                label.text = errors.get(component.id)[0]
                if not label.classes:
                    label.classes = ["govuk-error-message"]
                else:
                    label.classes.extend(["govuk-error-message"])

            # update group classes to show as error
            if not component.classes:
                component.classes = ["govuk-form-group--error", "govuk-error-message"]
            else:
                component.classes.extend(["govuk-form-group--error", "govuk-error-message"])

            cleaned_errors[component.id] = errors.get(component.id)

    return cleaned_errors


def nest_data(sent_data):
    """
    Nests strings into dictionaries eg
    {
        'site.name': 'SITE1'
    }
    becomes
    {
        'site': {
            'name': 'SITE1'
        }
    }
    """

    def _create_keys(d, keys, value):
        keys = keys.split(".")
        for k in keys[:-1]:
            if k not in d:
                d[k] = {}
            d = d[k]
        d[keys[-1]] = value

    data = {}

    for q, v in sent_data.items():
        _create_keys(data, q, v)

    return data


def flatten_data(d, parent_key="", sep="."):
    """
    Flattens dictionaries eg
    {
        'site': {
            'name': 'SITE1'
        }
    }
    becomes
    {
        'site.name': 'SITE1'
    }
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_data(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def conditional(condition: bool, obj, else_obj=None):
    """
    Returns the object depending on a condition
    Optionally: returns else_obj if it is set
    """
    if condition:
        return obj

    return else_obj


def heading_used_as_label(components):
    single_input = None

    if components:
        for component in components:
            if hasattr(component, "title") and hasattr(component, "name"):
                if single_input:
                    # If single_input has already been found, then we have multiple inputs
                    # and the heading cannot be used for multiple inputs
                    return None
                else:
                    single_input = component

    return single_input


def convert_to_markdown(text):
    if text:
        text = "<br>".join([markdown(item.strip(), extensions=["nl2br"]) for item in text.split("\n\n")])
        # Replace leading (<p>) & trailing (</p>) p tags as they are not needed
        text = text.replace("<p>", "")
        text = text.replace("</p>", "")
        text = text.replace(
            "<a", '<a class="govuk-link govuk-link--no-visited-state" rel="noreferrer noopener" target="_blank"'
        )
        return text
    else:
        return None


def handle_lists(data):
    """
    By default get() returns only one value, we use getlist() to return multiple values
    We indicate which components return a list by [] appended at the end of its name
    """
    temp_data = {}

    # If a key ends with [] remove the two characters, and instead
    # of doing a get() to get its values use a getlist() which returns all
    # of its values
    for key in data.keys():
        if key.endswith("[]"):
            temp_data[key[:-2]] = data.getlist(key)
        else:
            temp_data[key] = data.get(key)

    return temp_data


def get_all_form_components(form: Form):
    components = []
    for component in form.questions:
        if component and hasattr(component, "name"):
            components.append(component)
        if component and hasattr(component, "input_type") and component.input_type == "group":
            components.append(component)

        if getattr(component, "options", None):
            for option in component.options:
                if option and option.components:
                    for _component in option.components:
                        if _component and hasattr(_component, "name"):
                            components.append(_component)

    return components


def convert_form_to_summary_list_instance(form: Form):
    form.buttons[0].value = "Save and return"
    form.buttons[0].action = "return"
    return form


def insert_hidden_fields(data: dict, form: Form):
    for key, value in data.items():
        add = True

        # Only add hidden fields if the data isn't already being passed through a component
        for question in form.questions:
            if hasattr(question, "name"):
                if question.name == key or question.name[:-2] == key:
                    add = False

        if add:
            form.questions.insert(0, HiddenField(key, value))


def validate_data_unknown(object_pk, action, request, validated_data):
    if object_pk:
        return_value = action(request, object_pk, validated_data)  # noqa
    else:
        return_value = action(request, validated_data)  # noqa

    return return_value[0]


def convert_list_to_tree(items, key="key", value="value", children="children", exclude=None):
    return_value = []

    for item in items:
        node = TreeNode(item[key], item[value])
        if children in item:
            node.children = convert_list_to_tree(item[children], key, value, children, exclude)
        if not item.get(exclude):
            return_value.append(node)

    return return_value


def convert_dictionary_to_tree(dictionary, key="key", value="value", children="children", exclude=None):
    return_value = []

    for group, values in dictionary.items():
        return_value.append(TreeNode("", group, convert_list_to_tree(values, key, value, children, exclude)))

    return return_value
