import json


def pretty_json(data):
    try:
        return json.dumps(data, indent=4)
    except TypeError:
        return str(data)
