import importlib
import os
import re

LCS_PATTERN = "{% lcs '(.*)' %}"


def check_string_for_occurance(attribute, string):
    """
    Check that the given string variable i.e. `CASES.Page.TITLE` is found within a given module (strings.py).
    Checks each section of the path is found inside the module defined in the last iteration
    :param attribute: Python attribute to search
    :param string: Path to find (split into sections)
    :return: True/False
    """
    for path_section in string:
        attribute = attribute.__dict__.get(path_section)
        if isinstance(attribute, str):
            return True
        if not attribute:
            return False

    return True


def get_strings_package(base_dir):
    """
    Uses BASE_DIR to get the lite_content package
    i.e. /Users/user/lite-internal-frontend = lite_internal_frontend
    :return: strings package name
    """
    project_name = os.path.basename(base_dir)
    return project_name.replace("-", "_", 2)


def get_base_dir():
    """
    Get's the BASE_DIR from settings.
    Accounts for this file being called externally
    :return: str BASE_DIR value
    """
    try:
        from conf.settings import BASE_DIR
    except ModuleNotFoundError:
        # Fix for calling python file externally
        import sys

        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(parent_dir)
        from conf.settings import BASE_DIR
    return BASE_DIR


def get_all_lcs_strings(templates_folder):
    """
    Get all LCS strings from the HTML files in the given folder
    :param templates_folder: string path for the HTML folders
    :return: set of found LCS strings
    """
    strings = set()

    for root, _, files in os.walk(templates_folder):
        for file_name in files:
            if file_name.endswith(".html"):
                with open(f"{root}/{file_name}") as f:
                    lcs_strings = re.findall(LCS_PATTERN, f.read())
                    strings.update(lcs_strings)

    return strings


if __name__ == "__main__":
    not_found = []

    base_dir = get_base_dir()
    templates_folder = f"{base_dir}/templates"

    # Load strings package
    strings_package_name = get_strings_package(base_dir)
    strings_module = importlib.import_module(f"lite_content.{strings_package_name}.strings")

    # Check all strings are found
    lcs_strings = get_all_lcs_strings(templates_folder)
    for string in lcs_strings:
        if not check_string_for_occurance(strings_module, string.split(".")):
            not_found.append(string)

    if not_found:
        raise Exception(f"The following strings couldn't be found: {not_found}")
    else:
        print("No unused strings found")
