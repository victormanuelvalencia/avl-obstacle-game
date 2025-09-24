import json

def read_json(path):

    # Reads and returns the contents of a JSON file from the specified path.
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def write_json(data, path):

    # Writes the given data to a JSON file at the specified path.
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)