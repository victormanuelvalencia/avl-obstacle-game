import json

def read_json(path: str):
    """
    Read and return the contents of a JSON file.

    Args:
        path (str): Path to the JSON file.

    Returns:
        dict | list: Parsed JSON data.
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(data, path: str):
    """
    Write data to a JSON file at the specified path.

    Args:
        data (dict | list): Data to be serialized as JSON.
        path (str): Path to the output JSON file.
    """
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)