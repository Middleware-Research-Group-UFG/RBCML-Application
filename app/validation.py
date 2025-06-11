import re
import json
from datetime import datetime

from .database import db
from .user import User

def validate_string(input_str):
    pattern = re.compile(r'^[a-zA-Z0-9 _.@-]+$')
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

def validate_model(input_model, json_file):
    valid_keys = {
        "name": 64,
        "description": 256
    }

    return (
            len(input_model) == 2 and
            all(
                key in input_model and
                len(input_model[key]) <= max_len and
                validate_string(input_model[key]) and
                validate_model_json(json_file)
                for key, max_len in valid_keys.items()
            )
    )

def validate_model_json(input_model):    
    if len(input_model) != 2 or "roles" not in input_model or "connections" not in input_model:
        return False
    if not isinstance(input_model["roles"], list) or not isinstance(input_model["connections"], dict):
        return False

    roles = sorted(input_model["roles"])
    if not all(validate_string(role) for role in roles):
        return False

    connections = input_model["connections"]
    for connection_key, connection_value in connections.items():
        if not model_connection_is_valid(roles, connection_key, connection_value):
            return False

    return True

def validate_user(input_user):
    valid_keys = {
            "tag": 20,
            "name": 64,
            "email": 254,
            "password": 128
    }

    return (
            len(input_user) == 4 and
            all(
                key in input_user and
                len(input_user[key]) <= max_len and
                validate_string(input_user[key])
                for key, max_len in valid_keys.items()
            )
    )

def date_is_valid(date):
    try:
        datetime.fromisoformat(date)
        return True
    except:
        return False

def session_participants_are_valid(json_participants, id):
    participants = json.loads(json_participants)
    for participant in participants:
        if not validate_string(participant) or not db.exists(participant, 'Tag', 'User'):
            return False
    
    try:
        model_definition = json.loads(db.search(id, 'Id', 'Model')[0][3])
    except json.JSONDecodeError:
        return False
    model_roles = model_definition['roles']

    for roles in participants.values():
        if not isinstance(roles, list):
            return False
        for role in roles:
            if role not in model_roles:
                return False
    return True

def validate_session(input_session):
    valid_keys = [
            "Creator",
            "Id",
            "StartDate",
            "ExpirationDate",
            "Participants"
    ]

    return (
            len(input_session) == 5 and
            all(key in valid_keys for key in input_session) and
            validate_string(input_session['Creator']) and
            db.exists(input_session['Creator'], 'Tag', 'User') and
            isinstance(input_session['Id'], int) and
            db.exists(input_session['Id'], 'ModelId', 'Model') and
            date_is_valid(input_session['StartDate']) and
            date_is_valid(input_session['ExpirationDate']) and
            session_participants_are_valid(input_session['participants'], input_session['Id'])
    )

def validate_login(input_login):
    valid_keys = {
            "tag": 20,
            "password": 128
    }

    return (
            len(input_login) == 2 and
            all(key in valid_keys for key in input_login) and
            all(validate_string(value) for value in input_login.values()) and
            db.exists(input_login['tag'], 'tag', 'User') and
            User.login_match(input_login)
    )

