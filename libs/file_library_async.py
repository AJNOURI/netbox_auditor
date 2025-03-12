import json
from typing import Any, Literal, Union

import aiofiles
import yaml


# Read JSON file asynchronously
async def read_json(
    filename: str,
) -> Union[tuple[Literal[True], Any], tuple[Literal[False], str]]:
    """Read JSON file into Python data object asynchronously."""
    try:
        async with aiofiles.open(filename, "r", encoding="utf-8") as read_file:
            content = await read_file.read()
            return True, json.loads(content)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in file: {filename}, Error: {str(e)}"
    except OSError as e:
        return False, f"Could not open/read JSON file: {filename}, Error: {str(e)}"


# Write data to JSON file asynchronously
async def write_json(
    data: Any, filename: str
) -> Union[tuple[Literal[True], None], tuple[Literal[False], str]]:
    """Write data to JSON file asynchronously."""
    try:
        async with aiofiles.open(filename, "w", encoding="utf-8") as outfile:
            await outfile.write(json.dumps(data, indent=4))
        return True, None
    except (OSError, TypeError, ValueError) as error_f:
        return (
            False,
            f"Error while writing data to file: {filename}. Error details: {str(error_f)}",
        )


# Read YAML file asynchronously
async def read_yml(
    filename: str,
) -> Union[tuple[Literal[True], Any], tuple[Literal[False], str]]:
    """Read YAML file into Python data object asynchronously."""
    try:
        async with aiofiles.open(filename, "r", encoding="utf-8") as read_file:
            content = await read_file.read()
            return True, yaml.safe_load(content)
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in file: {filename}, Error: {str(e)}"
    except OSError as e:
        return False, f"Could not open/read YAML file: {filename}, Error: {str(e)}"
