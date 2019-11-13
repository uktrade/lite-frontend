import json

from conf.settings import BASE_DIR

JSON_PATH = BASE_DIR+'/lite_content/lite-internal-frontend/context_variables.json'
HIDDEN_VARS = ['valid', 'extends']
flattened_context_variables = []


def _get_valid_class_types(variables):
    valid_variables = {}
    for key, data in variables.items():
        if data['valid'] == "True":
            valid_variables[key] = data
    return valid_variables


def _get_build_order(json):
    keys = []
    for key, value in json.items():
        if 'extends' in value:
            keys.append(key)
    return keys


def _add_base_class_variables(json):
    for class_name in _get_build_order(json):
        for base_name in json[class_name]['extends']:
            json[class_name].update({base_name: json[base_name]})
    return json


def _remove_hidden_variables(dictionary):
    for var in HIDDEN_VARS:
        if var in dictionary:
            del dictionary[var]
    return dictionary


def _clean_dict(dictionary):
    dictionary = _remove_hidden_variables(dictionary)
    if 'variables' in dictionary:
        for var in dictionary['variables']:
            dictionary[var] = ''
        del dictionary['variables']
    for key, value in dictionary.items():
        if isinstance(value, dict):
            dictionary[key] = _clean_dict(value)
    return dictionary


def get_context_variables():
    with open(JSON_PATH, 'r') as f:
        variables = json.load(f)

    # Populate classes with any base class variables
    variables = _add_base_class_variables(variables)

    # Extract all object types we want to give to the user (using 'valid' key)
    variables = _get_valid_class_types(variables)

    # Remove all hidden variables and format as fully nested dict
    for key, value in variables.items():
        variables[key] = _clean_dict(value)

    return variables


def flatten_dict(dictionary, path):
    if path != '':
        path += '.'
    for key, value in dictionary.items():
        if isinstance(value, dict):
            flatten_dict(value, path + key)
        else:
            for variable in dictionary:
                flattened_context_variables.append(path + variable)


def get_flattened_context_variables():
    flatten_dict(get_context_variables(), '')
    return set(flattened_context_variables)


def get_sample_context_variables():
    return get_key_value_pair(get_flattened_context_variables())


def get_key_value_pair(data):
    return [{'key': item, 'representation': '{' + item + '}}'} for item in data]
