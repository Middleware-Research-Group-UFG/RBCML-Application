import jwt
from os import getenv
from pathlib import Path

path = Path(__file__).parent

def create(payload):
    with open(path/"keys/private_key.pem", "r") as file:
        private_key = file.read()
        return jwt.encode(payload, private_key, "RS256")

def decode(token, options):
    with open(path/"keys/public_key.pem", "r") as file:
        public_key = file.read()
        try:
            return jwt.decode(token, public_key, "RS256", options)
        except:
            return {}

def generate_default_decode_options(required):
    default = {
        "verify_signature": True,
        "verify_iat": "verify_signature",
        "verify_nbf": "verify_signature",
        "verify_exp": "verify_signature",
        "require": ["iat", "nbf", "exp"] + required
    }
    return default
