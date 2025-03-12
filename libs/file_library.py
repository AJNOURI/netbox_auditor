import json
from typing import Any, Literal, Union

import yaml


def read_json(
    filename: str,
) -> Union[tuple[Literal[True], Any], tuple[Literal[False], str]]:
    """Read JSON file into Python data objet"""
    try:
        with open(filename, encoding="utf-8") as read_file:
            return True, json.load(read_file)
    except OSError:
        return False, f"Could not open/read JSON file: {filename}"


def read_yml(
    filename: str,
) -> Union[tuple[Literal[True], Any], tuple[Literal[False], str]]:
    """Read YAML file into Python data objet"""
    try:
        with open(filename, encoding="utf-8") as read_file:
            return True, yaml.safe_load(read_file)
    except OSError:
        return False, f"Could not open/read YAML file: {filename}"


def write_json(
    data: Any, filename: str
) -> Union[tuple[Literal[True], None], tuple[Literal[False], str]]:
    """Write data to json file

    Args:
        data (python strcuture): data to save in json file format
        filename (string): result filename
    """
    try:
        with open(filename, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile)
        return True, None
    except Exception as error_f:
        return (
            False,
            f"___Error while writing data to file: {filename} \n___Error details: {str(error_f)}",
        )
