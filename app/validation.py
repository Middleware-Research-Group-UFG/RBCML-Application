import re


def validate_string(input_str):
    pattern = re.compile(r'^[a-zA-Z0-9 _.@]+$')
    return pattern.match(input_str)

def keys_are_sorted(keys):
    return all(keys[i] <= keys[i+1] for i in range(len(keys) - 1))

def model_connection_is_valid(roles, key, value):
    if not isinstance(value, list):
        return False

    key_roles = key.split("-")
    if len(value) != len(key_roles):
        return False
    if not all(role in roles for role in key_roles):
        return False
    if not keys_are_sorted(key_roles):
        return False
    
    for capabilities in value:
        if not isinstance(capabilities, list) or len(capabilities) != 8 or not all(isinstance(cap, bool) for cap in capabilities):
            return False
    
    return True


def validate_model(input_model):    
    if len(input_model) != 2 or "roles" not in input_model or "connections" not in input_model:
        return False
    if not isinstance(input_model["roles"], list) or not isinstance(input_model["connections"], dict):
        return False

    roles = sorted(input_model["roles"])
    if not all(validate_string(role) for role in roles):
        return False

    connections = input_model["connections"]
    if "-".join(roles) not in connections:
        return False
    for connection_key, connection_value in connections.items():
        if not model_connection_is_valid(roles, connection_key, connection_value):
            return False

    return True

def validate_user(input_user):
    valid_keys = {
            "tag": 20,
            "name" 64,
            "email": 254,
            "password": 128
    }

    return len(input_user) == 4 and
           all(
                key in input_user and
                len(input_user[key]) <= max_len and
                validate_string(input_user[key])
                for key, max_len in valid_keys.items()
               )

