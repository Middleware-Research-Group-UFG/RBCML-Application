import re

def validate_string(input_str):
    pattern = re.compile(r'^[a-zA-Z0-9 _.@]+$')
    if not pattern.match(input_str):
        raise ValueError("Invalid string. Only alphanumeric characters, spaces, '_', '.', and '@' are allowed.")
    return True
