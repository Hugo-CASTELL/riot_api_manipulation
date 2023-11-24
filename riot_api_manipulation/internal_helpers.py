import json as json_lib


def json_format_str(json):
    return json_lib.dumps(json, indent=2)
