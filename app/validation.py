import re
import json


def validate_string(input_str):
    pattern = re.compile(r'^[a-zA-Z0-9 _.@]+$')
    if not pattern.match(input_str):
        raise ValueError("Invalid string. Only alphanumeric characters, spaces, '_', '.', and '@' are allowed.")
    return True

def validate_json(input_json):
    
    if "roles" not in input_json or "connections" not in input_json:
        return False
    if not isinstance(input_json["roles"], list) or not isinstance(input_json["connections"], dict):
        return False

    roles = input_json["roles"]
    connections = input_json["connections"]

    
    for connection_key, connection_value in connections.items():
        key_roles = connection_key.split("-")

        for role in key_roles:
            if role not in roles:
                return False  

        if not isinstance(connection_value, list):
            return False  
        if len(connection_value) != len(key_roles):
            return False  

        for sublist in connection_value:
            if not isinstance(sublist, list) or len(sublist) != 8:
                return False  
            for item in sublist:
                if not isinstance(item, bool):
                    return False  

    return True  