import json
from constants import json_url
def read_json():
    """
    Reads the JSON data from the specified file.

    :return: The data read from the JSON file.
    """

    with open(json_url, 'r') as file:
        data = json.load(file)
    return data