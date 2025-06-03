from .database import db

class User:
    def __init__(self, tag, name, email):
        self.tag = tag
        self.name = name
        self.email = email

    @staticmethod
    def login_match(input_login):
        user_data = db.search(input_login['tag'], 'tag', 'User')[0]
        return (
                input_login['tag'] == user_data[0] and 
                input_login['password'] == user_data[3]
                )
